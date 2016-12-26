
import sys
from logger import one_time_report_logger
from OneTimeReport import OneTimeReport


class FADetectionBaselineOneTimeReport(OneTimeReport):
    def __init__(self, test_type, result_folder):
        OneTimeReport.__init__(self, test_type, result_folder)
        self.search_keyword = " "

    def get_keyword_and_sample_name(self, each_line):
        lower_line = str(each_line).lower()
        self.search_keyword = " "
        if lower_line.find("hs decision") != -1 or lower_line.find("decision") != -1:
            for item_ in self.sample_type_list:
                item = item_.lower()
                if lower_line.find(item) != -1:
                    self.search_keyword = item_
            if self.search_keyword == " ":
                return
            if lower_line.find(self.search_keyword) > lower_line.rfind("\\"):  # filter unmatch line
                return
            sample_name = lower_line[lower_line.rfind("\\") + 1:lower_line.find("]", lower_line.rfind("\\"))]
            if sample_name not in dict(self.sample_dict[self.search_keyword]).keys():
                self.sample_dict[self.search_keyword][sample_name] = "undetermined"
            if -1 != lower_line.find("[malicious]"):
                self.sample_dict[self.search_keyword][sample_name] = "malicious"
            if -1 != lower_line.find("[monitoring]"):
                if self.sample_dict[self.search_keyword][sample_name] == "undetermined":
                    self.sample_dict[self.search_keyword][sample_name] = "monitoring"

    def analyze_sample_dict(self):
        one_time_report_logger.info("analyze result and put the result into dict...")
        print "analyze result and put the result into dict..."
        total_malicious = 0.0
        total_malicious_rate = 0.0
        total_sample = 0
        if self.summary_line_flag:
            print "through scan every line to  statistics result..."
            for keyword in self.sample_type_list:
                self.test_info["result"][keyword]["total"] = len(self.sample_dict[keyword])
                self.test_info["result"][keyword]["malicious"] = (dict(self.sample_dict[keyword]).values()).count(
                    "malicious")
                self.test_info["result"][keyword]["monitoring"] = (dict(self.sample_dict[keyword]).values()).count(
                    "monitoring")
                self.test_info["result"][keyword]["undetermined"] = (dict(self.sample_dict[keyword]).values()).count(
                    "undetermined")
                total_malicious += float(self.test_info["result"][keyword]["malicious"])
                total_sample += self.test_info["result"][keyword]["total"]
                if len(self.sample_dict[keyword]):
                    result = float((dict(self.sample_dict[keyword]).values()).count("malicious")) / int(
                        len(self.sample_dict[keyword]))
                    self.test_info["result"][keyword]["malicious_rate"] = format(result, '.2%')
                else:
                    self.test_info["result"][keyword]["malicious_rate"] = format(0.0, '.2%')
            if total_sample:
                total_malicious_rate = total_malicious / total_sample
            self.test_info["result"]["total"]["total_malicious_rate"] = format(total_malicious_rate, '.2%')
            print "through scan every line to  statistics result completed!"
        else:
            print "through scan 'execution summary' to  statistics result..."
            print self.summary_log_dict
            for keyword in self.sample_type_list:   # self.summary_log_dict = {}
                support_decision_len = len(self.support_decision_type)
                self.test_info["result"][keyword]["malicious"] = 0
                if not support_decision_len:
                    return
                for log_num in range(len(self.summary_log_dict[keyword])/support_decision_len):
                    self.test_info["result"][keyword]["total"] = self.summary_log_dict[keyword][3]
                    self.test_info["result"][keyword]["malicious"] += self.summary_log_dict[keyword][2 + log_num*support_decision_len]
                    self.test_info["result"][keyword]["monitoring"] = self.summary_log_dict[keyword][1 + log_num*support_decision_len]
                    self.test_info["result"][keyword]["undetermined"] = self.summary_log_dict[keyword][0 + log_num*support_decision_len]
                total_malicious += float(self.test_info["result"][keyword]["malicious"])
                total_sample += self.test_info["result"][keyword]["total"]
                if self.test_info["result"][keyword]["total"] != 0:
                    result = float(self.test_info["result"][keyword]["malicious"]) / int(
                        self.test_info["result"][keyword]["total"])
                    self.test_info["result"][keyword]["malicious_rate"] = format(result, '.2%')
                else:
                    self.test_info["result"][keyword]["malicious_rate"] = format(0.0, '.2%')

            if total_sample:
                total_malicious_rate = total_malicious / total_sample
            self.test_info["result"]["total"]["total_malicious_rate"] = format(total_malicious_rate, '.2%')
            print "through scan 'execution summary' to  statistics result completed!"
        print "analyze result and put the result into dict completed!"

    def json_result_insert_to_template_str(self, json_obj):
        one_time_report_logger.info("fill json object into html template...")
        print "fill json object into html template..."
        html_str = str(self.html_template_str)
        html_str = html_str.replace("json_product_name", json_obj["test_info"]["product_name"])
        html_str = html_str.replace("json_test_name", json_obj["test_info"]['test_name'])
        html_str = html_str.replace("json_sal_version", json_obj["test_info"]["sal_version"])
        html_str = html_str.replace("json_sal_pattern_version", json_obj["test_info"]['sal_pattern_version'])
        html_str = html_str.replace("json_bep_version", json_obj["test_info"]["bep_version"])
        html_str = html_str.replace("json_bep_pattern_version", json_obj["test_info"]['bep_pattern_version'])
        html_str = html_str.replace("json_result_path",
                                    str(json_obj["test_info"]["result_path"]))
        for item in self.sample_type_list:
            html_str = html_str.replace("json_" + item + "_total_sample",
                                        str(json_obj["result"][item]["total"]))
            html_str = html_str.replace("json_" + item + "_malicious_sample",
                                        str(json_obj["result"][item]["malicious"]))
            html_str = html_str.replace("json_" + item + "_monitoring_sample",
                                        str(json_obj["result"][item]["monitoring"]))
            html_str = html_str.replace("json_" + item + "_undetermined_sample",
                                        str(json_obj["result"][item]["undetermined"]))
            html_str = html_str.replace("json_" + item + "_malicious_rate_sample",
                                        str(json_obj["result"][item]["malicious_rate"]))
        one_time_report_logger.info(html_str)
        return html_str


if "__main__" == __name__:
    # argv_result_folder = sys.argv[1]
    analyze = FADetectionBaselineOneTimeReport("sal_detection", "H:\\test_detection\\test_result")
    analyze.convert_result_to_json()
    analyze.convert_json_to_html()


