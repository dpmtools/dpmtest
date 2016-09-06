#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from random import randint
from lib.log import log_debug, log_err
from lib.util import login, install_driver
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER, USER_START, DRIVER_PACKAGE, DRIVER_START, PASSWORD, VERSION, DRIVER_NUM

if SHOW_TIME:
    from datetime import datetime

RANDOM_DRIVER = True

def test():
    log_debug('install', 'start testing ')
    login_cnt = 0
    install_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        uid, key = login(username, PASSWORD)
        if not uid or not key:
            log_err('install->login', 'failed to login %s.' % str(username))
            return False
        login_cnt += 1
        log_debug('install->login', 'login_cnt=%d' % login_cnt)
        if SHOW_TIME:
            log_debug('install->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
            start_time = datetime.utcnow()
        
        if RANDOM_DRIVER:
            driver_num = randint(40, DRIVER_NUM)
            package = DRIVER_PACKAGE + str(driver_num)
        else:
            package = DRIVER_PACKAGE + str(DRIVER_START + i)
        
        if not install_driver(uid, package, VERSION):
            log_err('instll', 'failed to install driver %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('install', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        install_cnt += 1
        log_debug('install', 'install_cnt=%d' % install_cnt)