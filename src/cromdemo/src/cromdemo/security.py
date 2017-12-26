# -*- coding: utf-8 -*-

from crom import subscription, adapter, sources, target
from cromlech.security import Unauthorized
from cromlech.security.interfaces import IProtectedComponent, ISecurityPredicate
from cromlech.security.meta import permissions
from zope.interface import Interface


accesses = {
    'admin': frozenset(('View', 'Manage')),
    'demo': frozenset(('View',)),
}


def check_permissions(component, interaction):
    perms = permissions.get(component) or tuple()
    if not perms:
        return
    
    for principal in interaction.principals:
        access = accesses.get(principal.id, None)
        if not access or not frozenset(perms) <= access:
            return Unauthorized
    return


@subscription
@sources(Interface)
@target(ISecurityPredicate)
def security_predicate(component, interaction):    
    return check_permissions(component, interaction)
