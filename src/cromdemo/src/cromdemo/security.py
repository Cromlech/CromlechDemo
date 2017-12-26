# -*- coding: utf-8 -*-

from crom import adapter, sources, target
from cromlech.security import Unauthorized
from cromlech.security.interfaces import IProtectedComponent
from cromlech.security.meta import permissions
from zope.interface import Interface


accesses = {
    'admin': frozenset(('View', 'Manage')),
    'demo': frozenset(('View',)),
}


@adapter
@sources(Interface)
@target(IProtectedComponent)
class SecurityPredicate(object):

    def __init__(self, component):
        self.component = component

    def __check_security__(self, interaction):    
        perms = permissions.get(self.component) or tuple()
        if not perms:
            return

        for principal in interaction.principals:
            access = accesses.get(principal.id, None)
            if not access or not frozenset(perms) <= access:
                return Unauthorized
        return
