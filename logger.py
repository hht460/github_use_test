
import logging.handlers
to_user = ["graysen_tong@trendmicro.com.cn", "haitao_hu@trendmicro.com.cn", "darwin_ye@trendmicro.com.cn",
           "david_qin@trendmicro.com.cn", "elodie_chen@trendmicro.com.cn", "michael_du@trendmicro.com.cn",
           "weimin_wu@trendmicro.com.cn", "wade_liu@trendmicro.com.cn", "Nico_jiang@trendmicro.com.cn"]
email_title = "Automation-Test-Report"

ONE_TIME_LOG_FILE = "one_time_report.log"
TREND_LOG_FILE = "trend_report.log"
SAL_REGRESSION_ONE_TIME_REPORT = "sal_regression_one_time_report.log"
BEP_REGRESSION_ONE_TIME_REPORT = "bep_regression_one_time_report.log"
SC_REGRESSION_ONE_TIME_REPORT = "sc_regression_one_time_report.log"

one_time_report_handler = logging.handlers.RotatingFileHandler(ONE_TIME_LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
one_time_report_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
one_time_report_formatter = logging.Formatter(one_time_report_fmt)
one_time_report_handler.setFormatter(one_time_report_formatter)
one_time_report_logger = logging.getLogger('one_time_report')
one_time_report_logger.addHandler(one_time_report_handler)
one_time_report_logger.setLevel(logging.DEBUG)

trend_report_handler = logging.handlers.RotatingFileHandler(TREND_LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
trend_report_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
trend_report_formatter = logging.Formatter(trend_report_fmt)
trend_report_handler.setFormatter(trend_report_formatter)
trend_report_logger = logging.getLogger('trend_report')
trend_report_logger.addHandler(trend_report_handler)
trend_report_logger.setLevel(logging.DEBUG)

'''
sal_regression_one_time_report_handler = logging.handlers.RotatingFileHandler(SAL_REGRESSION_ONE_TIME_REPORT, maxBytes=1024 * 1024, backupCount=5)
sal_regression_one_time_report_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
sal_regression_one_time_report_formatter = logging.Formatter(sal_regression_one_time_report_fmt)
sal_regression_one_time_report_handler.setFormatter(sal_regression_one_time_report_formatter)
sal_regression_one_time_report_logger = logging.getLogger('sal_regression_one_time_report')
sal_regression_one_time_report_logger.addHandler(sal_regression_one_time_report_handler)
sal_regression_one_time_report_logger.setLevel(logging.DEBUG)


bep_regression_one_time_report_handler = logging.handlers.RotatingFileHandler(BEP_REGRESSION_ONE_TIME_REPORT, maxBytes=1024 * 1024, backupCount=5)
bep_regression_one_time_report_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
bep_regression_one_time_report_formatter = logging.Formatter(bep_regression_one_time_report_fmt)
bep_regression_one_time_report_handler.setFormatter(bep_regression_one_time_report_formatter)
bep_regression_one_time_report_logger = logging.getLogger('bep_regression_one_time_report')
bep_regression_one_time_report_logger.addHandler(bep_regression_one_time_report_handler)
bep_regression_one_time_report_logger.setLevel(logging.DEBUG)


sc_regression_one_time_report_handler = logging.handlers.RotatingFileHandler(SC_REGRESSION_ONE_TIME_REPORT, maxBytes=1024 * 1024, backupCount=5)
sc_regression_one_time_report_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
sc_regression_one_time_report_formatter = logging.Formatter(sc_regression_one_time_report_fmt)
sc_regression_one_time_report_handler.setFormatter(sc_regression_one_time_report_formatter)
sc_regression_one_time_report_logger = logging.getLogger('bep_regression_one_time_report')
sc_regression_one_time_report_logger.addHandler(sc_regression_one_time_report_handler)
sc_regression_one_time_report_logger.setLevel(logging.DEBUG)
'''