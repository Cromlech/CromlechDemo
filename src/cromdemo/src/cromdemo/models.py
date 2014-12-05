# -*- coding: utf-8 -*-

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer, Interface
from zope.location import Location, locate
from zope.schema import Text, TextLine


class ILeaf(Interface):
    title = TextLine(title=u'title', required=True)
    body = Text(title=u'body', required=True)


@implementer(ILeaf)
class Leaf(Location):

    def __init__(self, title, body):
        self.title = title
        self.body = body


@implementer(IPublicationRoot)
class Root(dict):

    title = u"Demo Root"

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self['green'] = Leaf(u'Green leaf', u'A summer leaf')
        self['yellow'] = Leaf(u'Yellow leaf', u'An automn leaf')

    def __getitem__(self, key):
        item = dict.__getitem__(self, key)
        if item is not None:
            locate(item, self, key)
        return item
