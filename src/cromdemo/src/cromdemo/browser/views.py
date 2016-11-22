# -*- coding: utf-8 -*-

from . import tal_template, ITab
from .layout import ProtectedHeader, ContextualActions
from ..models import Root, Leaf

from crom import target
from dolmen.view import name, context, View
from dolmen.view import make_layout_response, view_component
from dolmen.viewlet import viewlet, Viewlet
from cromlech.browser import IURL, slot, view
from cromlech.browser.directives import title
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
@target(ITab)
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
@target(ITab)
@permission('ViewProtected')
class ProtectedLeafView(View):
    responseFactory = Response
    make_response = make_layout_response

    def render(self):
        return u'The protected area revealed !'


@viewlet
@slot(ProtectedHeader)
class WhoAmI(Viewlet):
    """Greets a logged in superuser on the index.
    """
    def render(self):
        username = self.request.environment['REMOTE_USER']
        return u"Welcome, master %s !" % username


@viewlet
@slot(ContextualActions)
class Tabs(Viewlet):
    template = tal_template('tabs.pt')

    def tabs(self):
        url = IURL(self.context, self.request)
        for name, view in self._tabs:
            label = title.get(view) or name
            if self.view.__class__ is view:
                active = True
            else:
                active = False
            yield {'active': active, 'title': label,
                   'url': '%s/%s' % (url, name)}

    def update(self):
        self._tabs = list(ITab.all_components(self.context, self.request))
