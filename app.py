# -*- coding: utf-8 -*-

import os
from loader import Configuration


with Configuration('config.json') as config:

    # We setup the cache for Chameleon templates
    os.environ["CHAMELEON_CACHE"] = config['templates']['cache']

    # Bootstrapping the Crom registry
    from crom import monkey, implicit
    monkey.incompat()
    implicit.initialize()

    # read the ZCML
    from cromlech.configuration.utils import load_zcml
    load_zcml(config['app']['zcml'])

    # load translation
    from cromlech.i18n import load_translations_directories
    load_translations_directories()

    # Create the application, including the middlewares.
    from cromdemo.wsgi import demo_application
    from cromlech.wsgistate.middleware import file_session_wrapper

    application = file_session_wrapper(
        demo_application,
        session_cache=config['session']['cache'],
        timeout=config['session']['timeout'])
