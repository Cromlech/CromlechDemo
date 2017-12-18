# -*- coding: utf-8 -*-

import os
from loader import Configuration


def get_key(path):
    from cromlech.jwt.components import JWTHandler
    if not os.path.isfile(path):
        with open(path, 'w+', encoding="utf-8") as keyfile:
            key = JWTHandler.generate_key()
            export = key.export()
            keyfile.write(export)
    else:
        key = JWTHandler.load_key_file(path)
    return key


with Configuration('config.json') as config:

    # We setup the cache for Chameleon templates
    os.environ["CHAMELEON_CACHE"] = config['templates']['cache']

    # Bootstrapping the Crom registry
    from crom import monkey, implicit
    monkey.incompat()
    implicit.initialize()

    # Getting the crypto key and creating the JWT service
    from cromlech.sessions.jwt import JWTCookieSession
    key = get_key(config['session']['jwt_key'])
    session_wrapper = JWTCookieSession(
        key, int(config['session']['timeout']))

    # read the ZCML
    from cromlech.configuration.utils import load_zcml
    load_zcml(config['app']['zcml'])

    # load translation
    from cromlech.i18n import load_translations_directories
    load_translations_directories()

    # Create the application, including the middlewares.
    from cromdemo.wsgi import demo_application
    application = session_wrapper(demo_application)
