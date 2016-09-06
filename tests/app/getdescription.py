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
    log_debug('get_description', 'start testing ')
    get_desc_cnt = 0
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
        
        message = json.dumps({'op':'get_description', 'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_description' != result['op'] or package != result['package'] or not  result['data']:
            log_err('get_description', 'failed to get the description of %s.' % str(package))
            return False
        title = result['data'][0]
        des = result['data'][1]
        if not title or not des:
            log_err('get_description', 'failed to get the description of %s, invalid return message.' % str(package))
            return False
        get_desc_cnt += 1
        log_debug('get_description', 'get_desc_cnt=%d' % get_desc_cnt)
        log_debug('get_description', 'the title and description of %s are %s and %s' % (str(package), str(title), str(des)))
        if SHOW_TIME:
            log_debug('get_description', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
