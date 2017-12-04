# -*- coding: utf-8 -*-

import os
import sys
import json

CH_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG = os.path.join(CH_DIR, 'config.json')


class Configuration(object):

    def __init__(self, filename, directory=None):
        if directory is None:
            directory = os.path.abspath(os.path.dirname(__file__))
        env = os.path.join(directory, filename)
        if not os.path.isfile(env):
            raise RuntimeError('Configuration file does not exist.')
        self.environ = env
        self.backup = sys.path[:]

    def __enter__(self):
        with open(self.environ, "r") as fd:
            env = json.load(fd)

        paths = env['paths']
        sys.path[0:0] = paths
        return env['conf']

    def __exit__(self, exc_type, exc_val, exc_tb):
        # we need to make something about error handling.
        sys.path = self.backup
