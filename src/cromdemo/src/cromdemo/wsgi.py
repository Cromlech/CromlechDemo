# -*- coding: utf-8 -*-

from functools import wraps

from crom import ComponentLookupError
from cromlech.browser import setSession
from cromlech.browser.interfaces import IView
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup, view_locator
from cromlech.i18n import EnvironLocale
from cromlech.security import ContextualProtagonist, Principal
from cromlech.security import component_protector
from cromlech.security import unauthenticated_principal
from cromlech.webob.request import Request

from .models import Root
from .auth import secured


logins = {
    'demo': 'demo',
    'admin': 'admin',
}


def query_view(request, context, name=""):
    view = IView.component(context, request, name=name)
    return view(context, request)


view_lookup = ViewLookup(view_locator(component_protector(query_view)))


def sessionned(app):
    @wraps(app)
    def with_session(environ, start_response):
        try:
            setSession(environ['session'])
            response = app(environ, start_response)
        finally:
            setSession()
        return response
    return with_session


def demo_application(environ, start_response):

    @sessionned
    @secured(logins, "CromlechDemo")
    def publisher(environ, start_response):
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

    return publisher(environ, start_response)
