#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, PASSWORD, USER, PACKAGE

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('has_package', 'start testing ')
    login_cnt = 0
    has_pkg_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        message = json.dumps({'op':'login', 'user':username, 'password':PASSWORD})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'login' != result['op'] or username != result['user'] or not  result['data']:
            log_err('login', 'failed to login %s.' % str(username))
            return False
        uid = result['data'][0]
        if not uid:
            log_err('has_package->login', 'failed to login %s, invalid uid or key.' % str(username))
            return False
        if SHOW_TIME:
            log_debug('has_package->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('has_package->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'op':'has_package', 'uid':uid,'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'has_package' != result['op'] or package != result['package'] or not  result['data']:
            log_err('has_package', 'failed to install app %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('has_package', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        has_pkg_cnt += 1
        log_debug('has_package', 'has_pkg_cnt=%d' % has_pkg_cnt)
        