# -*- coding: utf-8 -*-

from .models import Root
from barrel import cooper
from crom import monkey, implicit
from cromlech.configuration.utils import load_zcml
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from cromlech.security import component_protector
from cromlech.security import ContextualProtagonist, Principal
from cromlech.webob.request import Request
from cromlech.i18n import EnvironLocale, load_translations_directories


logins = [
    ('demo', 'demo'),
    ('admin', 'admin'),
    ]


view_lookup = ViewLookup(view_locator(component_protector(query_view)))


def demo_application(global_conf, zcml_file):

    # load crom
    monkey.incompat()
    implicit.initialize()

    # read the ZCML
    load_zcml(zcml_file)

    # load translation
    load_translations_directories()

    @cooper.basicauth(users=logins, realm="CromlechLite")
    def publisher(environ, start_response):

        with EnvironLocale(environ):
            request = Request(environ)
            root = Root()
            with ContextualProtagonist(Principal(environ['REMOTE_USER'])):
                publisher = DawnlightPublisher(view_lookup=view_lookup)
                response = publisher.publish(request, root, handle_errors=True)
                return response(environ, start_response)

    return publisher
