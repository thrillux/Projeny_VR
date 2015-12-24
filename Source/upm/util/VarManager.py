
import re
import sys
import os

import mtm.ioc.Container as Container
from mtm.ioc.Inject import Inject, InjectOptional
import mtm.ioc.Assertions as Assertions

class VarManager:
    _config = Inject('Config')

    '''
    Stores a dictionary of keys to values to replace path variables with
    '''
    def __init__(self, pythonDir, initialParams = None):
        self._params = initialParams if initialParams else {}
        self._params['PythonDir'] = pythonDir.replace('\\', '/')

        if self._config.mainPath:
            self._params['ConfigDir'] = os.path.dirname(self._config.mainPath).replace('\\', '/')

        configPaths = self._config.tryGetDictionary('PathVars', {})

        for key, value in configPaths.items():
            assert not key in self._params.keys()
            self._params[key] = value

    def hasKey(self, key):
        return key in self._params

    def get(self, key):
        assert key in self._params, 'Missing variable "{0}"'.format(key)
        return self._params[key]

    def add(self, key, value):
        assert not key in self._params
        self._params[key] = value

    def set(self, key, value):
        self._params[key] = value

    def tryGet(self, key):
        return self._params.get(key)

    def expandPath(self, text, extraVars = None, positionArgs = None):
        ''' Same as expand() except it cleans up the path to remove ../ '''

        # Forward slashes seem to work better with system helper
        return os.path.realpath(self.expand(text, extraVars, positionArgs))
        # This would be nice but causes something to go to hell
        # eg: scripts and plugins project directories get filled with the same files
        #.replace("\\", "/")

    def expand(self, text, extraVars = None, positionArgs = None):

        if not extraVars:
            extraVars = {}

        if not positionArgs:
            positionArgs = []

        allArgs = self._params.copy()
        allArgs.update(extraVars)

        try:
            while True:
                text = text.replace('[', '{').replace(']', '}')

                if not ('{' in text):
                    break

                text = text.format(*positionArgs, **allArgs)

        except KeyError as e:
            raise Exception('Unable to find key {0} in the list of known variables'.format(e))

        return text

