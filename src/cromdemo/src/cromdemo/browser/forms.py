# -*- coding: utf-8 -*-

from crom import target, order
from dolmen.forms.base import action, name, context, form_component
from dolmen.forms.base.errors import Error
from dolmen.forms.base import Fields, FAILURE
from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.interfaces import IPublicationRoot
from cromlech.security import permissions

from . import ITab, Form
from ..auth import Auth
from ..models import ILeaf, ILogin


@form_component
@name('edit')
@context(ILeaf)
@target(ITab)
@order(20)
@permissions('Manage')
class Edit(Form):
    fields = Fields(ILeaf)
    ignoreContent = False


@form_component
@name('login')
@context(Auth)
class Login(Form):

    fields = Fields(ILogin)

    @property
    def action_url(self):
        return self.request.url

    @action('Log me')
    def login(self):
        data, errors = self.extractData()
        if errors:
            form.errors = errors
            return FAILURE

        success = self.context.authenticate(
            data['username'], data['password'])
        if not success:
            self.errors.append(Error(
                title='Login failed',
                identifier=self.prefix,
            ))
            return FAILURE
        raise HTTPFound(self.request.url)
