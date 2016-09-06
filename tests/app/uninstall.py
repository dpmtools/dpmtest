#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PACKAGE, PASSWORD, PKG_NUM

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('uninstall', 'start testing ')
    login_cnt = 0
    uninstall_cnt = 0
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
        key = result['data'][1]
        if not uid or not key:
            log_err('uninstall->login', 'failed to login %s, invalid uid or key.' % str(username))
            return False
        if SHOW_TIME:
            log_debug('uninstall->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('uninstall->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        package = PACKAGE + str(50 + i)
        message = json.dumps({'op':'uninstall', 'uid':uid, 'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        result = json.loads(ret)
        if not result or 'uninstall' != result['op'] or uid != result['uid'] or not  result['data']:
            log_err('uninstall', 'failed to uninstall app %s' % str(package))
            return False
        uninstall_cnt += 1
        log_debug('uninstall', 'uninstall_cnt=%d' % uninstall_cnt)
        if SHOW_TIME:
            log_debug('uninstall', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
