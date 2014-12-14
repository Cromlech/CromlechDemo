# -*- coding: utf-8 -*-

from .models import Root
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from cromlech.security import component_protector, unauthenticated_principal
from cromlech.security import ContextualProtagonist, Principal
from cromlech.webob.request import Request
from cromlech.i18n import EnvironLocale


logins = [
    ('demo', 'demo'),
    ('admin', 'admin'),
    ]


view_lookup = ViewLookup(view_locator(component_protector(query_view)))


def demo_application(environ, start_response):

    with EnvironLocale(environ):
        request = Request(environ)
        root = Root()
        username = environ.get('REMOTE_USER')
        if username is not None:
            principal = Principal(username)
        else:
            principal = unauthenticated_principal
        with ContextualProtagonist(principal):
            publisher = DawnlightPublisher(view_lookup=view_lookup)
            response = publisher.publish(request, root, handle_errors=True)
            return response(environ, start_response)
