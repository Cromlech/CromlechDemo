# -*- coding: utf-8 -*-

from functools import wraps

from crom import ComponentLookupError
from cromlech.browser import setSession
from cromlech.browser.interfaces import IView
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup, view_locator
from cromlech.i18n import EnvironLocale
from cromlech.security import ContextualInteraction, Principal
from cromlech.security import removeFromInteraction, joinInteraction
from cromlech.security import getSecurityGuards, ContextualSecurityGuards
from cromlech.security import security_check, security_predication
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.webob.request import Request

from .models import Root
from .auth import secured


logins = {
    'demo': 'demo',
    'admin': 'admin',
    'grok': 'grok',
}


def secure_query_view(request, context, name=""):
    check, predict = getSecurityGuards()
    factory = IView.component(context, request, name=name)
    if predict is not None:
        factory = predict(factory)  # raises if security fails.
    view = factory(context, request)
    if check is not None:
        check(view)  # raises if security fails.
    return view


root = Root()
publisher = DawnlightPublisher(
    view_lookup=ViewLookup(view_locator(secure_query_view)),
).publish


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
            with ContextualSecurityGuards(security_predication, security_check):

                @secured(logins, "CromlechDemo")
                def publish(environ, start_response):
                    request = Request(environ)
                    username = environ.get('REMOTE_USER')
                    if username is not None:
                        principal = Principal(username)
                        removeFromInteraction(anonymous, interaction)
                        joinInteraction(principal, interaction)

                    response = publisher(request, root)
                    return response(environ, start_response)

                return publish(environ, start_response)
