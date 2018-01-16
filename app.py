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

# Getting the crypto key and creating the JWT service
from cromlech.sessions.jwt import key_from_file
from cromlech.sessions.jwt import JWTCookieSession

key = key_from_file(os.path.join(HERE, 'jwt.key'))
session_wrapper = JWTCookieSession(key, 300)

# read the ZCML
from cromlech.configuration.utils import load_zcml
load_zcml(os.path.join(HERE, 'app.zcml'))

# load translation
from cromlech.i18n import load_translations_directories
load_translations_directories()

# Adding the event dispatcher
from cromlech.events import setup_dispatcher
setup_dispatcher()

# Create the application, including the middlewares.
from cromdemo.wsgi import demo_application
application = session_wrapper(demo_application)

from waitress import serve
serve(application, listen='0.0.0.0:8080')
