#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""sal regresssion test script
"""

#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:     start sal regression test
#
# Author:      bella_meng
#
# Created:     12/08/2015
#-------------------------------------------------------------------------------
import pdb
import os
import sys
import argparse
from os.path import join
from utils.regression_cfg import RegressionConfig
from utils.send_email import SendEmail
# from preproc.getbuild_pattern import GetBuildPattern
from execution import *
from logging import debug as _d, info as _i, error as _e
from importlib import import_module

if __name__ == '__main__':
    from logging.config import fileConfig
    fileConfig('server.logging.cfg')
    _i('Enter SAL Test')
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(help= "sub-commands help", dest='test_name')
    # fixme by 
    sal_regression_parser = subparsers.add_parser('sal_regression')
    sc_regression_parser = subparsers.add_parser('sc_regression')
    bep_ti_regression_parser = subparsers.add_parser('bep_regression')
    sal_fa_parser = subparsers.add_parser('sal_fa')
    sal_detection_parser = subparsers.add_parser('sal_detection')
    sal_baseline_parser = subparsers.add_parser('sal_baseline')
    ti_pit = subparsers.add_parser('ti_pit')
    osce_pit = subparsers.add_parser('osce_pit')
    script_malware_detection_fa = subparsers.add_parser('script_malware_detection_fa')

    for subcommand in [sal_regression_parser,
                        sc_regression_parser,
                        bep_ti_regression_parser,
                        sal_fa_parser,
                        sal_detection_parser,
                        sal_baseline_parser,
                        ti_pit,
                        osce_pit,
                        script_malware_detection_fa]:        
        subcommand.add_argument('-a', '--actions', help="#-t -->test connection ;-b --> deploy build ;-s -->deploiy test case; -e -->execute ; -f -->fetch result", default = "-t -b -e -f")
        subcommand.add_argument('--skipfetchbuild', help="Fetchbuild from the server", default=True, action = "store_false")
        subcommand.add_argument('--skipsendmail', help="Send out result mail", default=True, action = "store_false")
        subcommand.add_argument('--skipruntest', help="Skip running test", default=False, action = "store_true")
        subcommand.add_argument('-C', '--configurations', help="Add a user configuration file", action = 'append', default = [r"cfg\sal_test.cfg"])
    args = parser.parse_args()
    _d('args is {0}'.format(args))
    args.configurations = args.configurations[:1] + [ join('cfg', '{0}.cfg'.format(args.test_name)) ] + args.configurations[1:]
    test_lib = import_module('sal_test.{0}.controller'.format(args.test_name))
    controller_cls = getattr(test_lib, 'Controller')
    controller_cls(args).run()
    _i('Exit SAL Test')