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
    log_debug('get_inst', 'start testing ')
    get_inst_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_PKG:
            cat_num = randint(0, len(CATEGORIES.keys()) - 1)
            cat_name = CATEGORIES.keys()[cat_num]
            pkg_num = randint(50, PKG_NUM)
            package = cat_name + '_' + PKG + str(pkg_num)
        else:
            package = PACKAGE + str(PKG_START + i)
        
        message = json.dumps({'op':'get_inst', 'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_inst' != result['op'] or package != result['package']:
            log_err('get_inst', 'failed to get the valid message' )
            return False
        get_inst_cnt += 1
        log_debug('get_inst', 'get_inst_cnt=%d' % get_inst_cnt)
        log_debug('get_inst', 'the number of %s has been installed is %s' % (str(package), str(result['data'])))
        if SHOW_TIME:
            log_debug('get_inst', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
