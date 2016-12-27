import os
from ConfigParser import ConfigParser


class ConfigReader(object):
    '''
    read config file
    '''
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_ftp_ip(self):
        if self.config.has_section('ftp_server'):
            ftp_ip = self.config.get("ftp_server", "ftp_ip")
            return ftp_ip
        return " "

    def get_ftp_port(self):
        if self.config.has_section('ftp_server'):
            ftp_port = self.config.get("ftp_server", "ftp_port")
            return ftp_port
        return " "

    def get_ftp_user_name(self):
        if self.config.has_section('ftp_server'):
            user_name = self.config.get("ftp_server", "user_name")
            return user_name
        return " "

    def get_ftp_user_pwd(self):
        if self.config.has_section('ftp_server'):
            user_pwd = self.config.get("ftp_server", "user_pwd")
            return user_pwd
        return " "

    def get_result_folder(self, project):
        if self.config.has_section(project):
            result_folder = self.config.get(project, "local_result_dir")
            return result_folder
        return " "

    def get_ftp_result_folder(self, project):
        if self.config.has_section(project):
            result_folder = self.config.get(project, "ftp_history_result_dir")
            return result_folder
        return " "

    def get_product_name(self):
        if self.config.has_section('test_info'):
            product_name = self.config.get("test_info", "productname")
            return product_name
        return " "

    def get_test_name(self):
        if self.config.has_section('test_info'):
            test_name = self.config.get("test_info", "test_name")
            return test_name
        return " "

    def get_ftp_host(self):
        if self.config.has_section('archive'):
            ftp_host = self.config.get("archive", "ftp_host")
            return ftp_host
        return " "

    def get_sal_version(self):
        if self.config.has_section('build_win32_sal'):
            sal_version = self.config.get("build_win32_sal", "version")
            return sal_version
        return " "

    def get_sal_pattern_version(self):
        if self.config.has_section('pattern_sal'):
            sal_pattern_version = self.config.get("pattern_sal", "version")
            return sal_pattern_version
        return " "

    def get_bep_version(self):
        if self.config.has_section('build_win32_bep'):
            bep_version = self.config.get("build_win32_bep", "version")
            return bep_version
        return " "

    def get_bep_pattern_version(self):
        if self.config.has_section('pattern_bep'):
            bep_pattern_version = self.config.get("pattern_bep", "version")
            return bep_pattern_version
        return " "

    def get_sample_category(self):
        if self.config.has_section('sample_category'):
            sample_category = self.config.options('sample_category')
            return sample_category
        return " "
