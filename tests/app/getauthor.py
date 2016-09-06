#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from random import randint
from lib.log import log_debug, log_err
from conf.category import CATEGORIES
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, PKG_START, PACKAGE

if SHOW_TIME:
    from datetime import datetime

PKG = 'bbb3'
PKG_NUM = 50
RANDOM_PKG = True

def test():
    log_debug('get_author', 'start testing ')
    auth_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_PKG:
            cat_num = randint(0, len(CATEGORIES.keys()) - 1)
            cat_name = CATEGORIES.keys()[cat_num]
            pkg_num = randint(40, PKG_NUM - 1)
            package = cat_name + '_' + PKG + str(pkg_num)
        else:
            package = PACKAGE + str(PKG_START + i)
        
        message = json.dumps({'op':'get_author', 'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_author' != result['op'] or package != result['package'] or not  result['data']:
            log_err('get_author', 'failed to get the author of %s ' % str(package))
            return False
        auth_cnt += 1
        log_debug('get_author', 'auth_cnt=%d' % auth_cnt)
        log_debug('get_author', 'the author of %s is %s' % (str(package), str(result['data'])))
        if SHOW_TIME:
            log_debug('get_author', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
