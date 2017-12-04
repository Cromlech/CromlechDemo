# -*- coding: utf-8 -*-

from . import ITab, Form
from ..models import ILeaf, ILogin
from ..auth import Auth

from crom import target, order
from dolmen.forms.base import name, context, form_component
from dolmen.forms.base import Fields, Action, Actions, FAILURE
from cromlech.browser.exceptions import HTTPFound
from cromlech.security import IProtectedComponent
from zope.interface import implementer


class LoginAction(Action):

    def available(self, form):
        return True

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        raise HTTPFound(form.request.url)


@form_component
@name('edit')
@context(ILeaf)
@target(ITab)
@order(20)
class Edit(Form):
    fields = Fields(ILeaf)


@form_component
@name('login')
@context(Auth)
@implementer(IProtectedComponent)
class Login(Form):
    fields = Fields(ILogin)
    actions = Actions(LoginAction(u'Log me'))

    @property
    def action_url(self):
        return self.request.url
