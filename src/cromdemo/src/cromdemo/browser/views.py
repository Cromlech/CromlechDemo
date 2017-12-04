# -*- coding: utf-8 -*-

from . import tal_template, ITab, Page
from .layout import ProtectedHeader, ContextualActions
from ..models import Root, Leaf

from crom import target, order
from crom.utils import sort_components
from dolmen.view import name, context, view_component
from dolmen.viewlet import viewlet, Viewlet
from cromlech.browser import IURL, slot
from cromlech.browser.directives import title
from cromlech.security import permissions, Unauthorized
from cromlech.security import IProtectedComponent
from zope.interface import implementer


@view_component
@name('index')
@context(Root)
class RootIndex(Page):
    template = tal_template('home.pt')


@view_component
@name('index')
@target(ITab)
@context(Leaf)
@order(10)
class LeafIndex(Page):
    template = tal_template('leaf.pt')


@view_component
@name('')
@context(Unauthorized)
class NoAcces(Page):

    def render(self):
        return u"No access for you !"


@view_component
@name('protected')
@context(Leaf)
@target(ITab)
@permissions('ViewProtected')
@implementer(IProtectedComponent)
class ProtectedLeafView(Page):

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


from cromlech.browser.predication import resolve_predications
from cromlech.security import Unauthorized, Forbidden


def sort_key(component):
    explicit = order.get_policy(component[1], order.dotted_name, 0)
    return (explicit, component[1].__module__, component[1].__class__.__name__)


@viewlet
@slot(ContextualActions)
class Tabs(Viewlet):
    template = tal_template('tabs.pt')

    def tabs(self):
        url = IURL(self.context, self.request)
        for id, view in self._tabs:
            try:
                resolve_predications(view, self.context, self.request)
            except (Unauthorized, Forbidden) as error:
                continue
    
            label = title.get(view) or id
            if self.view.__class__ is view:
                active = True
            else:
                active = False
            yield {'active': active, 'title': label,
                   'url': '%s/%s' % (url, id)}

    def update(self):
        self._tabs = sort_components(
            ITab.all_components(self.context, self.request), key=sort_key)
