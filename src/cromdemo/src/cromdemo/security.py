# -*- coding: utf-8 -*-

from crom import subscription, sources, target, order
from cromlech.browser.interfaces import IPredication
from cromlech.security import Unauthorized
from cromlech.security import queryInteraction
from cromlech.security.interfaces import IProtectedComponent, ISecurityCheck
from cromlech.security.meta import permissions


accesses = {
    'admin': set(('ViewProtected',)),
    }


class ISecurityPredication(IPredication, ISecurityCheck):
    pass


@order(1)
@subscription
@sources(IProtectedComponent)
@target(ISecurityPredication)
def security_predicate(component, *args):
    interaction = queryInteraction()
    if not interaction:
        raise Unauthorized
    
    protagonist = next(iter(interaction))
    access = accesses.get(protagonist.principal.id, None)
    if access is not None:
        perms = permissions.get(component) or tuple()
        if not perms:
            return
        elif frozenset(perms) <= access:
            return
    raise Unauthorized
