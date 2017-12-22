# -*- coding: utf-8 -*-

from functools import wraps

from crom import ComponentLookupError
from cromlech.browser import setSession
from cromlech.browser.interfaces import IView
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup, view_locator
from cromlech.i18n import EnvironLocale
from cromlech.security import ContextualProtagonist, Principal
from cromlech.security import component_protector, getSecureLookup
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.security import removeFromInteraction, joinInteraction
from cromlech.webob.request import Request

from .models import Root
from .auth import secured


logins = {
    'demo': 'demo',
    'admin': 'admin',
}


def secure_query_view(request, context, name=""):
    security_wrapper, lookup_exceptions = getSecureLookup()
    lookup = security_wrapper(IView.component)
    view = lookup(context, request, name=name)
    return view(context, request)


root = Root()
view_lookup = ViewLookup(view_locator(secure_query_view))
publisher = DawnlightPublisher(view_lookup=view_lookup).publish


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


@sessionned
def demo_application(environ, start_response):

    with EnvironLocale(environ):
        with ContextualInteraction(anonymous) as interaction:

            @secured(logins, "CromlechDemo")
            def publish(environ, start_response):
                request = Request(environ)
                username = environ.get('REMOTE_USER')
                if username is not None:
                    principal = Principal(username)
                    removeFromInteraction(anonymous, interaction)
                    joinInteraction(principal, interaction)
    
                response = publisher(request, root, handle_errors=True)
                return response

            return publish(environ, start_response)
