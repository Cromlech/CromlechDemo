# -*- coding: utf-8 -*-

import logging
from crom import subscription, sources, target
from zope.interface.interfaces import IObjectEvent
from cromlech.events import IEventHandler


logging.basicConfig(level=logging.INFO)


@subscription
@sources(IObjectEvent)
@target(IEventHandler)
def ObjectEventLogger(event):
    """An object has been fiddled with.
    This event handler will log in stdout the object events.
    """
    logging.info(
        'The object %r has been somehow touched. Event: %r' % (
            event.object, event))
