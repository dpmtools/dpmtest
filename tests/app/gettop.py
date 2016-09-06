#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from random import randint
from lib.log import log_debug, log_err
from conf.category import CATEGORIES
from websocket import create_connection
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

RANDOM_CAT = True

def test():
    log_debug('get_top', 'start testing ')
    get_top_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_CAT:
            cat_num = randint(0, len(CATEGORIES.keys()) - 1)
            cat_name = CATEGORIES.keys()[cat_num]
            if not CATEGORIES.has_key(cat_name):
                log_err('get_top', 'failed to get the top, invalid category is %s' % str(cat_name))
                return False
            cate = CATEGORIES[cat_name]
        else:
            cate = CATEGORY
        
        message = json.dumps({'op':'get_top', 'category':cate})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_top' != result['op'] or cate != result['category']:
            log_err('get_top', 'failed to get the top packages of %s' % str(cate))
            return False
        if SHOW_TIME:
            log_debug('get_top', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        get_top_cnt +=1
        log_debug('get_top', 'get_top_cnt=%d' % get_top_cnt)
        log_debug('get_top', 'top packages=%s' % str(result['data']))
