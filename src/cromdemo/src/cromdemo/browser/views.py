# -*- coding: utf-8 -*-

from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.exceptions import HTTPFound
from cromlech.security import Unauthorized
from zope.interface import Interface

from . import tal_template, ITab, Page
from ..models import Root, Leaf
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
