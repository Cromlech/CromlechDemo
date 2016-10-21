# -*- coding: utf-8 -*-

from crom import subscription, sources, target
from cromlech.security import Unauthorized
from cromlech.security.interfaces import ISecuredComponent, ISecurityCheck


accesses = {
    'admin': set(('ViewProtected',)),
    }


@subscription
@sources(ISecuredComponent)
@target(ISecurityCheck)
def view_security_checker(component, permission, interaction):
    """Implementation of our security policy
    """
    protagonist = next(iter(interaction))
    access = accesses.get(protagonist.principal.id, None)
    if access is not None:
        if permission is None:
            return
        elif permission in access:
            return
    return Unauthorized
