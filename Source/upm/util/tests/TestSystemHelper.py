
import sys
import os
import unittest

import mtm.ioc.Container as Container
from mtm.ioc.Inject import Inject
import mtm.ioc.Assertions as Assertions

from upm.util.VarManager import VarManager
from upm.util.SystemHelper import SystemHelper
from upm.log.Logger import Logger
from upm.config.ConfigXml import ConfigXml

class TestSystemHelper(unittest.TestCase):
    def setUp(self):
        Container.clear()

    def test1(self):
        Container.bind('Config').toSingle(ConfigXml)
        Container.bind('VarManager').toSingle(VarManager)
        Container.bind('SystemHelper').toSingle(SystemHelper)
        Container.bind('Logger').toSingle(Logger)

        self._test1(Container.resolve('SystemHelper'))

    def _test1(self, sysHelper):
        '''
        @type sysHelper: SystemHelper
        '''
        output = sysHelper.executeAndReturnOutput('echo 5')
        self.assertEqual(output, '5')

        self.assertTrue(sysHelper.fileExists(os.path.realpath(__file__)))
        self.assertTrue(not sysHelper.fileExists('sadfcvzxvasdf'))

        #sysHelper.executeAndWait('cmd /c mklink')
        sysHelper.executeAndWaitWithParams(None, 'cmd', '/c', 'mklink')

if __name__ == '__main__':
    unittest.main()


