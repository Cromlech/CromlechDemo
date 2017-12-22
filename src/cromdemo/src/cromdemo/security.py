# -*- coding: utf-8 -*-

from crom import adapter, sources, target
from cromlech.security import Unauthorized
from cromlech.security.interfaces import IProtectedComponent
from cromlech.security.meta import permissions
from zope.interface import Interface


accesses = {
    'admin': set(('ViewProtected',)),
    }


@adapter
@sources(Interface)
@target(IProtectedComponent)
class SecurityPredicate(object):

    def __init__(self, component):
        self.component = component

    def __check_security__(self, interaction):    
        protagonist = next(iter(interaction))
        perms = permissions.get(self.component) or tuple()
        if not perms:
            return
        
        access = accesses.get(protagonist.principal.id, None)
        if access and frozenset(perms) <= access:
            return
        raise Unauthorized
