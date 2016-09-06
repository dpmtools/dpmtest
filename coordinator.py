#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import zerorpc
from conf.servers import SRV_ADDR
from conf.dpmtest import CLI_PORT, SRV_PORT, CLIENTS, MODE

class Coordinator(object):
    def __init__(self):
        self._cnt = 0
        self._addr = []
        
    def join(self, addr):
        self._cnt += 1
        self._addr.append(addr)
        if self._cnt == CLIENTS:
            for i in self._addr:
                cli = zerorpc.Client()
                cli.connect('tcp://%s:%d' % (i, CLI_PORT))
                cli.start_test(MODE)

if __name__ == '__main__':
    s = zerorpc.Server(Coordinator())
    s.bind("tcp://%s:%d" % (SRV_ADDR, SRV_PORT))
    s.run()