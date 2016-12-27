#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ, linesep
from ConfigParser import ConfigParser
from StringIO import StringIO
from pdb import set_trace
import StringIO
default_version = '0.0.0'

def add_val2section(cfg, section, name, value):
    if value and value != default_version:
        cfg.add_section(section)
        cfg.set(section, name, value)
    else:
        print('[warning] {0}\'s version is not set in environment!'.format(section))

def build_sal_regression_cfg(env):
	productname =  env.get('SAL_product_name', 'sc')
	sal_pattern_version = env.get('SAL_PATTERN_VERSION', default_version)
	sal_build_version = env.get('SAL_BUILD_VERSION', default_version)
	bep_build_version = env.get('BEP_BUILD_VERSION', default_version)
	bep_pattern_version = env.get('BEP_PATTERN_VERSION', default_version)
	custom_config = env.get('CUSTOM_CONFIG', '')
	cfg_name = r'{0}.cfg'.format(productname)
	cfg = ConfigParser()
	# read the configuration of the product
	cfg.read(cfg_name)
	add_val2section(cfg, 'test_info', 'productname', productname)
	add_val2section(cfg, 'pattern_sal', 'version', sal_pattern_version)
	add_val2section(cfg, 'pattern_bep', 'version', bep_pattern_version)
	add_val2section(cfg, 'build_win32_sal', 'version', sal_build_version)
	add_val2section(cfg, 'build_win64_sal', 'version', sal_build_version)
	add_val2section(cfg, 'build_win32_bep', 'version', bep_build_version)
	add_val2section(cfg, 'build_win64_bep', 'version', bep_build_version)
	# read custom_config
	if custom_config:
		buf = StringIO.StringIO(custom_config)
		cfg.readfp(buf)
	return cfg

def build_cfg(env):
	test_name = env.get('SAL_test_name', 'sal_regression')
	return build_sal_regression_cfg(env)
	# raise Exception('SAL_test_name({0}) is not supported'.format(test_name))

def main(cfg_file_path):
	#print environ
	with open(cfg_file_path, 'w') as f:
                build_cfg(environ).write(f)
	pass

if __name__ == '__main__':
	main('temp.cfg')
	print 'creat-cfg-py'
