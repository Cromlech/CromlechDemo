# -*- coding: utf-8 -*-

from . import tal_template
from .layout import ProtectedHeader
from ..models import Root, Leaf

from dolmen.view import name, context, View
from dolmen.view import make_layout_response, view_component
from dolmen.viewlet import viewlet, Viewlet
from cromlech.browser import slot, view
from cromlech.webob.response import Response
from cromlech.security import secured_component, permission, Unauthorized


@view_component
@name('index')
@context(Root)
class RootIndex(View):
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('home.pt')


@view_component
@name('index')
@context(Leaf)
class LeafIndex(View):
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('leaf.pt')


@view_component
@name('')
@context(Unauthorized)
class NoAcces(View):
    responseFactory = Response
    make_response = make_layout_response

    def render(self):
        return u"No access for you !"


@view_component
@secured_component
@name('protected')
@context(Leaf)
@permission('ViewProtected')
class ProtectedLeafView(View):
    responseFactory = Response
    make_response = make_layout_response

    def render(self):
        return u'The protected area revealed !'


@viewlet
@slot(ProtectedHeader)
@view(RootIndex)
class WhoAmI(Viewlet):
    """Greets a logged in superuser on the index.
    """
    def render(self):
        username = self.request.environment['REMOTE_USER']
        return u"Welcome, master %s !" % username
