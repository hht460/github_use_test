# -----------------------------------------------
# Name = OneTimeReport.py
# Author = Graysen Tong
# for summary result of Baseline test / FA test / Detection test
# Date = 16/08/2016
# -----------------------------------------------

import os
import json
from json2html import *
from HTMLtemplate import html_result_str
from collections import OrderedDict
from GetConfigInfo import ConfigReader
from logger import one_time_report_logger
import ConfigParser
import re


class OneTimeReport(object):
    def __init__(self, test_type, result_folder):
        self.type = test_type
        self.ftp_path = " "
        self.result_path = result_folder  # self.cfg.get_result_folder(self.type)
        self.test_info = OrderedDict()
        self.json_name = " "
        self.html_result_path = " "
        self.json_file_path = " "
        self.json_obj = " "
        self.client_cfg_path = ''
        self.html_template_str = html_result_str
        self.sample_dict = {}
        self.sample_type_list = []
        self.summary_log_dict = {}
        self.scan_summary_test_name_list = []
        self.summary_line_flag = True  # 'True' enter scan every line pattern | 'False' enter scan execution summary
        self.summary_flag = True
        self.test_name = ''
        self.current_log_type = ""
        self.support_decision_type = []
        self.do_not_scan_log_list = []

    def find_target_file_and_scan_it(self, result_path):
        # pre process
        if self.test_name in self.scan_summary_test_name_list:
            for pre_parent, pre_dir_name, pre_file_name in os.walk(result_path):
                for pre_item in pre_file_name:
                    print pre_item
                    if ("log" in pre_item) and (pre_item not in self.do_not_scan_log_list):
                        self.summary_flag = False
                        with open(os.path.join(pre_parent, pre_item), 'rb') as pre_fd:
                            pre_file_list = pre_fd.readlines()
                            for every_line in pre_file_list[len(pre_file_list) - 150:]:
                                if every_line.find("execution summary") != -1:
                                    self.summary_flag = True
                                    print "find execution summary!"
                                    continue
                            if not self.summary_flag:
                                print "not find execution summary"
                                break
                if not self.summary_flag:
                    print "not find execution summary"
                    break
            self.summary_line_flag = not self.summary_flag
        print "whether enter 'every line' to scan? ", self.summary_line_flag
        print "whether enter 'execution summary' to scan? ", not self.summary_line_flag

        for parent, dir_name, file_name in os.walk(result_path):
            for _item in file_name:
                if "final.cfg" in _item:
                    self.client_cfg_path = os.path.join(parent, _item)
                if ("log" in _item) and (_item not in self.do_not_scan_log_list):
                    one_time_report_logger.info("scan file:" + _item)
                    one_time_report_logger.info("scan path:" + os.path.join(parent, _item))
                    print "scan path:" + os.path.join(parent, _item)
                    self.scan_result_file(os.path.join(parent, _item))
            one_time_report_logger.info("final_cfg path:" + self.client_cfg_path)

    def init_test_result_info(self):
        one_time_report_logger.info("start init_test_result_info!")
        one_time_report_logger.info("result folder:" + self.result_path)
        for parent, dir_name, file_name in os.walk(self.result_path):
            for _item in file_name:
                if "final.cfg" in _item:
                    self.client_cfg_path = os.path.join(parent, _item)
        self.sample_type_list = self.get_sample_type()  # get sample_type_list
        self.test_info["test_info"] = OrderedDict()
        self.test_info["test_info"]["result_path"] = self.result_path
        self.test_info["result"] = OrderedDict()

        for typ in self.sample_type_list:
            self.test_info["result"][typ] = OrderedDict()
            self.sample_dict[typ] = OrderedDict()
            self.summary_log_dict[typ] = []
        self.test_info["result"]['total'] = OrderedDict()
        print dict(self.summary_log_dict).keys()
        print self.summary_log_dict
        if os.path.exists(self.client_cfg_path):
            client_cfg = ConfigReader(self.client_cfg_path)
            self.ftp_path = client_cfg.get_ftp_host()
            self.test_info["test_info"]["product_name"] = client_cfg.get_product_name()
            self.test_info["test_info"]["test_name"] = client_cfg.get_test_name()
            self.test_info["test_info"]["sal_version"] = client_cfg.get_sal_version()
            self.test_info["test_info"]["sal_pattern_version"] = client_cfg.get_sal_pattern_version()
            self.test_info["test_info"]["bep_version"] = client_cfg.get_bep_version()
            self.test_info["test_info"]["bep_pattern_version"] = client_cfg.get_bep_pattern_version()
        # self.ftp_path+"/"+self.test_info["test_info"]["product_name"] + "/" + self.test_info["test_info"]["test_name"]
        else:
            one_time_report_logger.info("ERROR:did not get the client config!!")
            assert "did not get the client config!!"
        one_time_report_logger.info(self.test_info)
        self.test_name = self.test_info["test_info"]["test_name"]
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.client_cfg_path)
        self.scan_summary_test_name_list = cfg.get('scan_summary_test_name_list', 'scan_summary_test_name').split(";")
        self.support_decision_type = cfg.get('support_decision_type', 'support_test_result_type').split(";")
        self.do_not_scan_log_list = cfg.get('do_not_scan_log_list', 'do_not_scan_log').split(";")

    def scan_result_file(self, file_path):      # 'file_path' just one log
        one_time_report_logger.info("scanning each line of result file...")
        one_time_report_logger.info(file_path)
        print "scanning each line of result file..."
        if not self.summary_line_flag:
            self.last_line_add_target_value(self.get_current_log_type(file_path))
        else:
            with open(file_path, 'rb') as fd:
                each_line = fd.readline()
                while each_line:
                    self.scan_each_line(each_line)
                    each_line = fd.readline()

    def scan_each_line(self, each_line):         # we do not use keyword here
        self.get_keyword_and_sample_name(each_line)

    def get_keyword_and_sample_name(self, each_line):
        pass

    def analyze_sample_dict(self):
        pass

    def analyze_result(self):
        self.init_test_result_info()
        self.find_target_file_and_scan_it(self.result_path)

    def convert_result_to_json(self):
        one_time_report_logger.info("convert result into json file...")
        print "convert result into json file..."
        self.analyze_result()
        self.analyze_sample_dict()
        self.json_name = "one_time_report.json"
        self.json_file_path = os.path.join(self.result_path, self.json_name)
        one_time_report_logger.info(self.json_file_path)
        one_time_report_logger.info(self.test_info)
        with open(self.json_file_path, 'w+') as json_file:
            json_file.write(json.dumps(self.test_info, indent=4))
        one_time_report_logger.info("convert result into json file completed!")
        print "convert result into json file completed!"
        # print self.test_info

    def convert_json_to_html(self):
        one_time_report_logger.info("convert json file to html...")
        print "convert json file to html..."
        json_obj = self.convert_json_file_to_json_object(self.json_file_path)
        str_obj = str(self.json_file_path).replace(".json", ".html")
        index = str_obj.rfind("\\")
        html_name = str_obj[index + 1:len(str_obj)]
        global html_end
        global html_head
        with open(os.path.join(self.result_path, "one_time_report.html"), 'w+') as data:
            data.write(json2html.convert(json=json_obj, table_attributes="border=\"1\" width=\"100%\" ""class=\"table table-bordered table-hover\" bgcolor=rgb(233,233,233)"))
        with open(os.path.join(self.result_path, html_name), 'r+') as str_data:
            str_result = str_data.read()
            new_result = html_head + str_result + html_end
        with open(os.path.join(self.result_path, html_name), 'w+') as new_data:
            new_data.write(new_result)
        print "convert json file to html completed"

    def convert_json_file_to_json_object(self, json_file_path):
        one_time_report_logger.info("start convert_json_file_to_json_object")
        with open(json_file_path, 'r+') as data:
            self.json_obj = json.load(data)
        return self.json_obj

    def get_sample_type(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.client_cfg_path)
        sample_type_list = []
        if cfg.has_section('sample_category'):
            for sample_type in cfg.options('sample_category'):
                sample_type_list.append(cfg.get('sample_category', sample_type).replace("\\\\", "\\"))
            return sample_type_list
        else:
            return ["flash", "html", "java", "pdf"]

    def json_result_insert_to_template_str(self, json_obj):
        return ""
        pass

    def last_line_add_target_value(self, file_lines):   # 'file_lines' just is log last 40 lines
        # search last 40 line
        if not self.summary_line_flag:
            for item in ["[undetermined]=", "[monitoring]=", "[malicious]=", "Scan All Count"]:
                find_target_type_flag = False
                for line in file_lines:
                    if (line.find(item)) != -1:
                        find_target_type_flag = True
                        if re.search('\[(\d+)\]', line):
                            lst = re.findall('\d+', line)
                            self.summary_log_dict[self.current_log_type].append(int(lst[0]))
                            print item + ' ' + str(lst[0])
                if not find_target_type_flag:
                    self.summary_log_dict[self.current_log_type].append(0)
                print self.summary_log_dict
        else:
            return

    def get_current_log_type(self, file_path):       # only deal with one log and fetch sample type
        with open(file_path, 'rb') as fd:
            file_list = fd.readlines()               # 'file_list' is all log msg
            if len(file_list) > 20:                  # log line must more 20
                for line in file_list[:10]:
                    if line.find('Argument') != -1:
                        print line
                        for sample_type in self.summary_log_dict.keys():
                            if (len(line)-2) != (line.find(sample_type) + len(sample_type)):
                                print sample_type
                                continue
                            else:
                                print sample_type
                                self.current_log_type = sample_type
                                break
                return file_list[len(file_list)-150:]  # fetch last 40 lines
            else:
                return []


html_head = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<style type="text/css">
body,table{
font-size:20px;
}
table{
empty-cells:show;
border-collapse: collapse;
margin:0 auto;
}
td{
height:30px;
}
h1,h2,h3{
font-size:20px;
margin:0;
padding:0;
}
.table{
border:1px solid #cad9ea;
color:#666;
}
.table th {
background-repeat:repeat-x;
height:30px;
}
.table td,.table th{
border:1px solid #cad9ea;
padding:0 1em 0;
}
.table tr.alter{
background-color:#f5fafe;
}
</style>
</head>
<body>
<div align="center">
<h1 align="center"> TEST RESULT REPORT </h1>
<hr />
</div>

<div>
'''

html_end = '''
</div>
</body>
</html>
'''
