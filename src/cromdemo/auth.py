# -*- coding: utf-8 -*-

from functools import wraps
from cromlech.security import Principal
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.browser import getSession
from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer
from zope.location import Location


@implementer(IPublicationRoot)
class Auth(dict, Location):

    def authenticate(self, username, password):
        if username in self:
            if password == self[username]:
                session = getSession()
                session['user'] = username
                return True
        return False


def logout(session=None):
    if session is None:
        session = getSession()
    if 'user' in session:
        session.clear()
        return True
    return False


def secured(app):

    @wraps(app)
    def secure_application(environ, start_response, default=anonymous):
        session = getSession()
        if session is not None and 'user' in session:
            environ['REMOTE_USER'] = username = session['user']
            principal = Principal(username)
        else:
            principal = default
        return app(environ, start_response, principal)

    return secure_application
