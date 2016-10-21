# -*- coding: utf-8 -*-

import cgi
from cromlech.auth import BasicAuth
from cromlech.browser import IPublicationRoot, IResponseFactory
from cromlech.browser import getSession
from cromlech.webob import Request
from dolmen.view import query_view
from zope.interface import implementer
from zope.location import Location


try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO


def logout(session=None):
    if session is None:
        session = getSession()
    if 'REMOTE_USER' in session:
        del session['REMOTE_USER']
        return True
    return False


@implementer(IPublicationRoot, IResponseFactory)
class Auth(Location, BasicAuth):

    def __init__(self, users, realm):
        BasicAuth.__init__(self, users, realm)

    def valid_user(self, username, password):
        pwd = self.users.get(username, None)
        return pwd is not None and pwd == password

    def session_dict(self, environ):
        return getSession()

    def save_session(self):
        pass

    def not_authenticated(self, environ, start_response):
        request = Request(environ)
        view = query_view(request, self, name='login')
        if view is None:
            raise NotImplementedError
        response = view()
        return response(environ, start_response)

    def username_and_password(self, environ):
        """Pull the creds from the form encoded request body."""
        # How else can I tell if this is an auth request before reading?
        if environ.get('CONTENT_LENGTH'):
            clen = int(environ['CONTENT_LENGTH'])

            sio = StringIO(environ['wsgi.input'].read(clen))
            fs = cgi.FieldStorage(fp=sio,
                                  environ=environ,
                                  keep_blank_values=True)
            sio.seek(0)
            environ['wsgi.input'] = sio
            if fs.getlist("form.action.log-me"):
                try:
                    username = fs["form.field.username"].value
                    password = fs["form.field.password"].value
                    return username, password
                except KeyError:
                    pass # silence

        return '', ''

    def __call__(self, app):
        def security_traverser(environ, start_response):
            if self.authenticate(environ):
                return app(environ, start_response)
            return self.not_authenticated(environ, start_response)
        return security_traverser


def secured(users, realm):
    """Decorator to secure my apps with.
    """
    def deco(app):
        auth = Auth(users, realm)
        return auth(app)
    return deco
