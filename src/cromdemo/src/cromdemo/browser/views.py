# -*- coding: utf-8 -*-

from . import tal_template, ITab, Page
from .layout import SiteHeader, AdminHeader, ContextualActions
from ..models import Root, Leaf

from crom import target, order
from crom.utils import sort_components
from dolmen.view import name, context, view_component
from dolmen.viewlet import viewlet, Viewlet
from cromlech.browser import IURL, slot
from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.directives import title
from cromlech.security import permissions, Unauthorized
from cromlech.security import getSecurityGuards
from zope.interface import implementer, Interface
from ..auth import logout


@view_component
@name('logout')
@context(Interface)
class Logout(Page):

    def update(self):
        logout()

    def render(self):
        raise HTTPFound(location='/')


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
        return "No access for you !"


@viewlet
@slot(SiteHeader)
class Cromlech(Viewlet):

    def render(self):
        return "<h1>Cromlech</h1>"

    
@viewlet
@slot(AdminHeader)
class WelcomeMaster(Viewlet):
    """Greets a logged in superuser on the index.
    """
    def render(self):
        username = self.request.environment['REMOTE_USER']
        return "<p>Welcome, master %s !</p>" % username


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
            yield {
                'active': self.view.__class__ is view,
                'title': title.get(view) or id,
                'url': '%s/%s' % (url, id),
            }

    def update(self):
        tabs = ITab.all_components(self.context, self.request)
        predict, _ = getSecurityGuards()
        if predict is not None:
            tabs = (
                (name, tab) for name, tab in tabs
                if predict(tab, swallow_errors=True) is not None)

        self._tabs = sort_components(tabs, key=sort_key)
        self.available = len(self._tabs) > 0
