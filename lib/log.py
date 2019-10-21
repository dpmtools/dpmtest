#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from conf.dpmtest import LOG_ERROR, LOG_DEBUG

def log_err(location, text):
    if LOG_ERROR:
        print('%s: %s' % (location, text))
        
def log_debug(location, text):
    if LOG_DEBUG:
        print('%s: %s' % (location, text))
