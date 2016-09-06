#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import os
import zlib
import json
from lib.log import log_debug, log_err
from lib.util import login, upload, DRIVER
from conf.dpmtest import  TEST_ROUNDS, SHOW_TIME, USER, USER_START, DRIVER_PACKAGE, DRIVER_START, PASSWORD, VERSION

if SHOW_TIME:
    from datetime import datetime

DRIVER_PATH = '/root/testfiles/driver/driver4'
    
def test():
    log_debug('upload', 'start testing ')
    login_cnt = 0
    upload_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        uid, key = login(username, PASSWORD)
        if not uid or not key:
            log_err('upload->login', 'failed to login %s.' % str(username))
            return False
        login_cnt += 1
        log_debug('upload->login', 'login_cnt=%d' % login_cnt)
        
        package = DRIVER_PACKAGE + str(DRIVER_START + i)
        if not upload(DRIVER_PATH, uid, package, VERSION, DRIVER, key):
            log_err('upload', 'failed to upload driver %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('upload', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        upload_cnt += 1
        log_debug('upload', 'upload_cnt=%d' % upload_cnt)