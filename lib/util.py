#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import os
import zlib
import json
import fcntl
import yaml
import struct
import socket
import types
import shutil
import hashlib
import tempfile
import commands
from random import randint
from log import log_debug, log_err
from conf.path import PATH_DRIVER 
from component.rpcclient import RPCClient
from conf.servers import SERVER_FRONTEND, SERVER_MANAGER
from conf.dpmtest import MANAGER_PORTS, FRONTEND_PORT, IFACE

APP = 'app'
DRIVER = 'driver'
APT = 'apt-get'
PIP = 'pip'
INSTALLERS = [APT, PIP]

def get_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return  socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', IFACE[:15]))[20:24])

def get_frontend():
    n = randint(0, len(SERVER_FRONTEND) - 1)
    return SERVER_FRONTEND[n]

def get_manager():
    n = randint(0, len(SERVER_MANAGER) - 1)
    server =  SERVER_MANAGER[n]
    return server

def get_port():
    n = randint(0, len(MANAGER_PORTS) - 1)
    return MANAGER_PORTS[n]

def get_md5(text):
    if type(text) is types.StringType:
        tmp = hashlib.md5()   
        tmp.update(text)
        return tmp.hexdigest()
    else:
        log_err('util', 'failed to get md5')

def login(user, password):
    user = str(user)
    pwd = get_md5(str(password))
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT)
    uid, key = rpcclient.request('login', user=user, pwd=pwd)
    return (str(uid), str(key))

def dump_content(dirname, has_children=True):
    content = {}
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isdir(path):
            if name not in [APP, DRIVER]:
                raise Exception('failed to dump content')
            if has_children:
                res = dump_content(path, has_children=False)
                if res:
                    content.update({name: res})
            else:
                raise Exception('failed to dump content')
        else:
            with open(path) as f:
                buf = f.read()
            if name == 'description':
                buf = buf.replace('\n', ',')[:-1]
                res = buf.split(',')
                buf = {}
                for i in res:
                    info = i.split(':')
                    buf.update({info[0]: info[1][1:]})
                buf = yaml.dump(buf)
            content.update({name:buf})
    return content

def upload(path, uid, package, version, typ, key):
    content = dump_content(path)
    buf = zlib.compress(json.dumps(content))
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT, uid, key)
    ret  = rpcclient.request('upload', uid=uid, package=package, version=version, buf=buf, typ=typ)
    if ret:
        return True
    else:
        log_err('util', 'failed to upload, uid=%s, package=%s, version=%s, typ=%s' % (str(uid), str(package), str(version), str(typ)))
        return False

def install(uid, package, version, typ):
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT)
    if typ == DRIVER:
        content = None
    ret = rpcclient.request('install', uid=uid, package=package, version=version, typ=typ, content=content)
    if not ret:
        log_err('util', 'failed to install, uid=%s, package=%s, version=%s, typ=%s' % (str(uid), str(package), str(version), str(typ)))
        return
    return ret

def install_driver(uid, package, version=None):
    driver_path = os.path.join(PATH_DRIVER, package)
    if os.path.exists(driver_path):
        shutil.rmtree(driver_path)
    ret = install(uid, package, version, DRIVER)
    if not ret:
        log_err('util', 'failed to install driver, uid=%s, driver=%s, version=%s' % (str(uid), str(package), str(version)))
        return False
    dirname = tempfile.mkdtemp()
    try:
        buf = json.loads(zlib.decompress(ret))
        dep = buf['dep']
        if not _check_dep(dep):
            log_err('util', 'failed to install driver, invalid dependency, uid=%s, driver=%s, version=%s' % (str(uid), str(package), str(version)))
            return False
        driver = buf['driver']
        if driver:
            src = os.path.join(dirname, 'driver')
            os.mkdir(src)
            filenames = driver.keys()
            for name in filenames:
                filepath = os.path.join(src, name)
                with open(filepath, 'wb') as f:
                    f.write(driver[name])
            shutil.copytree(src, driver_path)
    finally:
        shutil.rmtree(dirname)
    return True

def _check_dep(buf):
    if not buf:
        return
    
    dep = yaml.load(buf)
    if not dep:
        return
    cmds = []
    for i in dep:
        installer = dep[i].get('installer')
        if installer not in INSTALLERS:
            log_err('util', 'failed to check dependency, invalid installer')
            return
        cmd = '%s install %s' % (installer, i)
        version = dep[i].get('version')
        if version:
            if installer == APT:
                cmd += '=%s' % version
            elif installer == PIP:
                cmd += '==%s' % version
        cmds.append(cmd)
    
    for cmd in cmds:
         status, output = commands.getstatusoutput(cmd)
         if status != 0:
             log_err('util', 'failed to check dependency')
             return
    
    return True
