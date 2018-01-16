# -*- coding: utf-8 -*-

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer, Interface
from zope.location import Location, locate
from zope.schema import Text, TextLine, Password


class ILogin(Interface):

    username = TextLine(
        title='Username', required=True)

    password = Password(
        title='Password', required=True)


class ILeaf(Interface):

    title = TextLine(
        title='Title', required=True)

    body = Text(
        title='Body', required=True)


@implementer(ILeaf)
class Leaf(Location):

    def __init__(self, title, body):
        self.title = title
        self.body = body


@implementer(IPublicationRoot)
class Root(dict, Location):

    title = u"Demo Root"

    def __getitem__(self, key):
        item = dict.__getitem__(self, key)
        if item is not None:
            locate(item, self, key)
        return item
