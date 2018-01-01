# -*- coding: utf-8 -*-

from crom import subscription, sources, target
from cromlech.browser.interfaces import IView
from cromlech.security import Unauthorized
from cromlech.security import getSecurityGuards
from cromlech.security.interfaces import ISecurityPredicate
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


def secure_query_view(request, context, name=""):
    check, predict = getSecurityGuards()
    factory = IView.component(context, request, name=name)
    if predict is not None:
        factory = predict(factory)  # raises if security fails.
    view = factory(context, request)
    if check is not None:
        check(view)  # raises if security fails.
    return view
