#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import json
from random import randint
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port, login, upload, APP
from conf.dpmtest import  TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PACKAGE, PASSWORD, VERSION, CATEGORY

if SHOW_TIME:
    from datetime import datetime

PAGE_SIZE = 8
PATH = '/root/testfiles/cat0_bbb3'

def test():
    log_debug('upload', 'start testing ')
    login_cnt = 0
    upload_cnt = 0
    get_pkgs_details_cnt = 0
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
        package = PACKAGE + str(50 + i)
        if not upload(PATH, uid, package, VERSION, APP, key):
            log_err('upload', 'failed to upload app %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('upload', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        upload_cnt += 1
        log_debug('upload', 'upload_cnt=%d' % upload_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'op':'get_counter', 'category':CATEGORY})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_counter' != result['op'] or CATEGORY != result['category'] or not  result['data']:
            log_err('get_counter', 'failed to get counter')
            return False
        counter = result['data']
        if not counter:
            log_err('get_counter', 'failed to get the total number of %s ' % str(CATEGORY))
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
        message = json.dumps({'op':'get_packages_details', 'category':CATEGORY, 'rank':rank})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_packages_details' != result['op'] or CATEGORY != result['category'] or rank != result['rank'] or not result['data']:
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
        
        
        
