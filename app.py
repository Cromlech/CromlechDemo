# -*- coding: utf-8 -*-

import os

HERE = os.path.dirname(os.path.abspath(__file__))

# We setup the cache for Chameleon templates
template_cache = os.path.join(HERE, 'cache')
if not os.path.exists(template_cache):
    os.makedirs(template_cache)
os.environ["CHAMELEON_CACHE"] = template_cache

# Bootstrapping the Crom registry
from crom import monkey, implicit
monkey.incompat()
implicit.initialize()

# Read the ZCML
# This is not a mandatory stage.
# Actually, what the ZCML loading does is grok the packages
# This can be done manually, using `crom.configure`
from cromlech.configuration.utils import load_zcml
load_zcml(os.path.join(HERE, 'app.zcml'))

# Load translation
# This is needed only if we want internationalization
from cromlech.i18n import load_translations_directories
load_translations_directories()

# Adding the event dispatcher
# Use only if you have event handlers or plan to have some.
from cromlech.events import setup_dispatcher
setup_dispatcher()

# Getting the crypto key and creating the JWT service
# We chose the JWT signed cookie for the demo
# `cromlech.sessions` proposed different backends.
# Or you can use the WSGI session middleware of your choice.
from cromlech.sessions.jwt import key_from_file
from cromlech.sessions.jwt import JWTCookieSession

key = key_from_file(os.path.join(HERE, 'jwt.key'))
session_wrapper = JWTCookieSession(key, 300)

# Create the application, including the middlewares.
from cromdemo.wsgi import demo_application
application = session_wrapper(demo_application)
