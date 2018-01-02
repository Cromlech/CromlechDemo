# -*- coding: utf-8 -*-

from crom import target, order
from cromlech.browser import IURL
from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.interfaces import IPublicationRoot
from cromlech.security import permissions
from dolmen.forms.base import Fields, FAILURE
from dolmen.forms.base import action, name, context, form_component
from dolmen.forms.base import apply_data_event
from dolmen.forms.base.errors import Error

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

    @action('Apply')
    def apply(self):
        data, errors = self.extractData()
        if errors:
            form.errors = errors
            return FAILURE

        content = self.getContent()
        apply_data_event(self.fields, content, data)
        raise HTTPFound(IURL(content, self.request))


@form_component
@name('login')
@context(Auth)
class Login(Form):

    fields = Fields(ILogin)
    ignoreContent = True

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
