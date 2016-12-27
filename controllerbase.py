#!python
# -*- coding: utf-8 -*-

from logging import debug as _d, info as _i, error as _e
from utils.regression_cfg import RegressionConfig
from utils.send_email import SendEmail
from shutil import rmtree
# from preproc.getbuild_pattern import GetBuildPattern
from .execution import *
from logging import debug as _d, info as _i, error as _e, exception as _ex
from sal.repack import main as sal_repack
import json
import time
from shutil import copyfile
from os.path import join, basename, exists
from os import makedirs
from utils.archive import archive
from os import environ
from saltest.utils.vm_ctrl import VMCtrl 
from saltest.utils.staf_ctrl import StafCtrl 

class ControllerBase(object):
    """A test controller"""
    def __init__(self, args):
        super(ControllerBase, self).__init__()
        self.args = args

    def fetch_build(self):
        output_dir = self.cfg_insts.builds_dir
        if exists(output_dir):
            rmtree(output_dir)
        builds = sal_repack.main(self.cfg_insts.cfg, output_dir)
        print builds
        _i('repacked builds is {0}'.format(builds))
        print 'buildinfo_path:',self.cfg_insts.buildinfo_path
        with open(self.cfg_insts.buildinfo_path, 'w') as buildinfo_file:
            json.dump(builds, buildinfo_file, indent = 2)

    def analyze_result(self):
        raise NotImplementedError('analyze_result is not implemented!')


    def revertClientEnv(self, client_group, cfg_handle):
        #revert client snapshot
        if not cfg_handle.isRevertNeeded():
            _i("Do not need to revert client env")
            return True

        _i("Need to revert client env")
        vmctrl = VMCtrl(cfg_handle.getVIXWorkDir())
        esxi_info = cfg_handle.getEsxiServerInfo()
        fail_clients = ""
        for client_name in client_group:
            client_vm_info = cfg_handle.getClientVMInfo(client_name)
            #revert vm
            _d("revert client vm: %s" %client_name)
            if client_vm_info is None:
                _e("no snapshot or path: %s" %client_name)
                fail_clients += client_name+","
                continue
            if not vmctrl.revertVM(esxi_info, client_vm_info):
                _e("revert vm fail: %s" %client_name)
                fail_clients += client_name+","
                continue

        fail_clients = fail_clients.rstrip(",")
        if fail_clients:
            _i("Revert Fail, issue clients: %s" %fail_clients)
            return False
        else:
            _i("All VM Revert Done")
            return True
        

    def checkStafConnection(self, client_group, cfg_handle):
        #ping client vm to check connection is ok
        _i("Check client staf connection")
        fail_clients = ""
        stafctrl = StafCtrl()
        for client_name in client_group:
            #test connection, ping vm
            success = False
            _d("ping client: %s" %client_name)
            for i in range(1, 5):
                client_ip = cfg_handle.getClientIp(client_name)
                _d("ping vm: %s %s %d" % (client_name, client_ip,i))
                if not stafctrl.pingHost(client_ip):
                    _e("ping vm fail: %s %s" % (client_name, client_ip))
                    _e("continue to ping vm %s %s" % (client_name, client_ip))
                    time.sleep(10)
                    continue
                else:
                    success = True
                    break
            if not success:
                fail_clients += client_name + ","
            
        fail_clients = fail_clients.rstrip(",")
        if fail_clients:
            _i("Check Staf Fail, issue clients: %s" %fail_clients)
            return False
        else:
            _i("All Staf Connection is OK")
            return True


    def run(self):
        args = self.args
        assert hasattr(args, 'configurations')
        _i('Enter {test_name} main'.format(test_name = args.test_name))
        self.test_name = args.test_name
        # TODO: move me to __init__
        cfg_files = args.configurations
        # TODO: save configurations to result
        self.cfg_insts = cfg_insts = RegressionConfig(cfg_files)
        cfg_insts.cfg.set('test_info', 'test_name', self.test_name)
        with open(cfg_insts.final_cfg, 'w') as cfg_file:
            cfg_insts.cfg.write(cfg_file)
        execute_script = cfg_insts.cfg.get('client', 'test_script')
        actions = args.actions
        productname = cfg_insts.getProductname()
        client_group = cfg_insts.getWorkClientGroupInfo() #client machine name
        
        #init client environment and check staf status
        is_succ = self.revertClientEnv(client_group, cfg_insts)
        assert is_succ, "revert client env fail"

        is_succ = self.checkStafConnection(client_group, cfg_insts)
        assert is_succ, "check staf connection fail"

        # make sure the required folder exists.

        if exists(cfg_insts.getResultDir()):
            rmtree(cfg_insts.getResultDir())        
        makedirs(cfg_insts.getResultDir())

        # bak the configurations
        copyfile(
            cfg_insts.final_cfg,
            join(
                cfg_insts.getResultDir(),
                basename(cfg_insts.final_cfg)))

        if args.skipfetchbuild:
            self.fetch_build()
        else:
            _i('Skip fetching build')
        
        # bak the buildinfo
        copyfile(
            cfg_insts.buildinfo_path,
            join(
                cfg_insts.getResultDir(),
                basename(cfg_insts.buildinfo_path)))


        #stt staf process
        insts = {}
        _i('client_group is {0}'.format(client_group))
        for i in client_group:
                cmd = "python -m main.STAFTrigger %s %s %s %s" % (i, execute_script, actions, ' '.join(["-C %s" % (c,) for c in args.configurations]))
                _d("cmd of {0} \t:{1}".format(i, cmd))
                se = SingleExecution(cmd, name=i)
                insts[i] = se
        processes = []
        for k,v in insts.items():
                processes.append(SerialExecutions([insts[k]]))

        p = ParallelExecutions(processes)
        p.setInterval(8.0)
        if not args.skipruntest:        
            p.run()
        else:
            _i('Skip running test')

        # there is fetchresult action
        if '-f' in args.actions:
            try:
                self.analyze_result()
            except Exception:
                _ex('exception when analyze_result')
        else:
            _i('Do not need to anlayze result since not fetching results!')

        if not args.skipsendmail:
            email_server.sendResult("SAL Regression Test Result", result_file) 
        _i('Exit {test_name} main'.format(test_name = args.test_name))

        buildid = environ.get('BUILD_NUMBER', 0)
        archive(cfg_insts.getResultDir(), buildid)
