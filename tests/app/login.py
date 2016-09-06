#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, USER, PASSWORD

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('login', 'start testing ')
    login_cnt = 0
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
            log_err('login', 'failed to login %s, invalid uid or key.' % str(username))
            return False
        if SHOW_TIME:
            log_debug('login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('login', 'login_cnt=%d' % login_cnt)
        
