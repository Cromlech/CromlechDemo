# -*- coding: utf-8 -*-

from cromlech.browser.interfaces import IView
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup, view_locator
from cromlech.i18n import EnvironLocale
from cromlech.security import ContextualInteraction
from cromlech.security import ContextualSecurityGuards
from cromlech.security import security_check, security_predication
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.webob.request import Request

from .models import Root
from .auth import Auth, sessionned, secured
from .security import secure_query_view


root = Root()
auth = Auth({
    'demo': 'demo',
    'admin': 'admin',
    'grok': 'grok',
})

publisher = DawnlightPublisher(
    view_lookup=ViewLookup(view_locator(secure_query_view)),
).publish


@secured
def publish(environ, start_response, principal):
    request = Request(environ)
    with ContextualInteraction(principal):
        if principal is anonymous:
            login = IView.adapt(auth, request, name='login')
            login.update()
            response = login()
        else:
            response = publisher(request, root)
        return response(environ, start_response)


@sessionned
def demo_application(environ, start_response):
    with ContextualSecurityGuards(security_predication, security_check):
        with EnvironLocale(environ):
            return publish(environ, start_response, anonymous)
