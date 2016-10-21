# -*- coding: utf-8 -*-

from . import tal_template, ITab
from .layout import ProtectedHeader
from ..models import ILeaf, ILogin
from ..auth import Auth

from crom import target
from dolmen.forms.base import name, context, form_component
from dolmen.forms.base import Fields, Form, Action, Actions
from dolmen.view import make_layout_response
from cromlech.webob.response import Response
from cromlech.browser.exceptions import HTTPFound
from cromlech.security import secured_component


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
@secured_component
class Edit(Form):
    responseFactory = Response
    make_response = make_layout_response
    fields = Fields(ILeaf)


@form_component
@name('login')
@context(Auth)
class Login(Form):
    responseFactory = Response
    make_response = make_layout_response

    fields = Fields(ILogin)
    actions = Actions(LoginAction(u'Log me'))

    @property
    def action_url(self):
        return self.request.url
