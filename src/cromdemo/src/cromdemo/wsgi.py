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


# Root serves as a publication root, for the authenticated users.
# It behaves like a dict, but it will locate objects upon retrieval
# using the `__getitem__` method.
root = Root()


# Auth serves as a context for the `Login` form.
# It behaves like a dict but has a simple `authenticate` method
# used by the form.
auth = Auth({
    'demo': 'demo',
    'admin': 'admin',
    'grok': 'grok',
})


# The publisher is a 2 times component that is in charge of looking up
# the model and the view, given an URL.
# It relies on traversers to handle the publishing.
# Here, we provide a custom way to retrieve views, using a security-aware
# function.
# See `dawnlight` and `cromlech.dawnlight` for more information.
publisher = DawnlightPublisher(
    view_lookup=ViewLookup(view_locator(secure_query_view)),
).publish


@sessionned
@secured
def publish(environ, start_response, principal):
    request = Request(environ)

    # The `Interaction` serves as the "who" in the security model.
    # The security model relies on 2 elements : the "who" and the "how".
    # The "how" is provided by the security guards declared with the
    # ContextualSecurityGuards context manager, in the `demo_application`
    # function.
    with ContextualInteraction(principal):
        if principal is anonymous:
            # This is a simple usecase of "members-only" for the demo :
            # We do not want anonymous users.
            # But we could continue and rely on the security checks to raise
            # security errors and redirect on the login form.
            login = IView.adapt(auth, request, name='login')
            login.update()
            response = login()
        else:
            # The user is authenticated, we can call the publisher to
            # traverse and publish our objects.
            response = publisher(request, root)

        # We cook the WSGI response and return it.
        # Our application ends here.
        return response(environ, start_response)


def demo_application(environ, start_response):

    # Security guards are the security context of the application
    # They have 2 layers : predicate and checks.
    # This context is thread-bound.
    # See `cromlech.security` documentation for more information.
    with ContextualSecurityGuards(security_predication, security_check):
        # We set the language of the application, extracting the
        # language preferences from the browser request.
        # See `cromlech.i18n` for more information.
        with EnvironLocale(environ):
            # We call our publishing function.
            # We provide a default user that can be overriden
            # by the `secured` decorator that will extract the
            # cached user from the session.
            return publish(environ, start_response, anonymous)
