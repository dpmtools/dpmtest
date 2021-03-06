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
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

PAGE_SIZE = 8
RANDOM_CAT = True

def test():
    log_debug('get_packages_details', 'start testing ')
    get_pkgs_details_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_CAT:
            cat_num = randint(0, len(CATEGORIES.keys()) - 1)
            cat_name = CATEGORIES.keys()[cat_num]
            if not CATEGORIES.has_key(cat_name):
                log_err('get_packages_details', 'failed to get the category, invalid category is %s' % str(cat_name))
                return False
            cate = CATEGORIES[cat_name]
        else:
            cate = CATEGORY
        
        message = json.dumps({'op':'get_counter', 'category':cate})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_counter' != result['op'] or cate != result['category'] or not  result['data']:
            log_err('get_counter', 'failed to get counter')
            return False
        counter = result['data']
        if not counter:
            log_err('get_counter', 'failed to get the total number of %s ' % str(cate))
            return False
        if SHOW_TIME:
            log_debug('get_counter', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        log_debug('get_counter', 'counter=%s' % str(counter))
        if int(counter) < 1:
            rank = 0
        else:
            rank = randint(0, (int(counter)  + PAGE_SIZE  - 1) / PAGE_SIZE - 1)
        log_debug('get_counter', 'rank=%d' % rank)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'op':'get_packages_details', 'category':cate, 'rank':rank})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_packages_details' != result['op'] or cate != result['category'] or rank != result['rank'] or not  result['data']:
            log_err('get_packages_details', 'failed to get packages details')
            return False
        ret = result['data']
        for item in ret:
            if not item['pkg'] or not item['title'] or not item['auth']:
                log_err('get_packages_details', 'failed to get valid details')
                return False
        if SHOW_TIME:
            log_debug('get_packages_details', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        get_pkgs_details_cnt += 1
        log_debug('get_packages_details', 'get_pkgs_details_cnt=%d' % get_pkgs_details_cnt)
        log_debug('get_packages_details', 'packages_details=%s' % str(ret))
