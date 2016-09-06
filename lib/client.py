#
# Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from lib import mode
from lib.util import get_addr
from threading import Thread
from conf.servers import SRV_ADDR
from conf.dpmtest import CLI_PORT, SRV_PORT

class Client(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mode = None
    
    def start_test(self, name):
        self.mode = name
        self.start()
    
    def run(self):
        if self.mode == mode.APP_REGISTER:
            from tests.app.register import test
        elif self.mode == mode.APP_LOGIN:
            from tests.app.login import test
        elif self.mode == mode.APP_UPLOAD:
            from tests.app.upload import test
        elif self.mode == mode.APP_INSTALL:
            from tests.app.install import test
        elif self.mode == mode.APP_UNINSTALL:
            from tests.app.uninstall import test
        elif self.mode == mode.APP_GETAUTHOR:
            from tests.app.getauthor import test
        elif self.mode == mode.APP_GETCATEGORIES:
            from tests.app.getcategories import test
        elif self.mode == mode.APP_COUNTER:
            from tests.app.getcounter import test
        elif self.mode == mode.APP_GETDESCRIPTION:
            from tests.app.getdescription import test
        elif self.mode == mode.APP_GETINST:
            from tests.app.getinst import test
        elif self.mode == mode.APP_GETINSTALLEDPACKAGES:
            from tests.app.getinstalledpackages import test
        elif self.mode == mode.APP_GETPACKAGESDETAILS:
            from tests.app.getpackagesdetails import test
        elif self.mode == mode.APP_GETTOP:
            from tests.app.gettop import test
        elif self.mode == mode.APP_GETTOPDETAILS:
            from tests.app.gettopdetails import test
        elif self.mode == mode.APP_HASPACKAGE:
            from tests.app.haspackage import test
        elif self.mode == mode.DRV_UPLOAD:
            from tests.driver.upload import test
        elif self.mode == mode.DRV_INSTALL:
            from tests.driver.install import test
        else:
            raise Exception('invalid mode')
        
        test()
