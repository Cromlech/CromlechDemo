# -*- coding: utf-8 -*-

import crom

from . import tal_template
from .resources import lite
from cromlech.browser import IRequest, ILayout
from cromlech.i18n import getLocale
from cromlech.security import secured_component, permission
from cromlech.webob.response import Response
from dolmen.viewlet import ViewletManager, viewlet_manager
from js.jqueryui import black_tie
from zope.interface import Interface


@viewlet_manager
@secured_component
@permission('ViewProtected')
class ProtectedHeader(ViewletManager):
    """Priviledied user only manager
    """
    pass


@viewlet_manager
class ContextualActions(ViewletManager):
    pass


@crom.component
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class LiteLayout(object):

    responseFactory = Response
    template = tal_template('layout.pt')

    title = u"Cromlech Lite"

    def __init__(self, request, context):
        self.context = context
        self.request = request
        self.target_language = getLocale()

    def namespace(self, **extra):
        namespace = {
            'context': self.context,
            'request': self.request,
            'layout': self,
            }
        namespace.update(extra)
        return namespace

    def __call__(self, content, **namespace):
        lite.need()
        black_tie.need()
        environ = self.namespace(**namespace)
        environ['content'] = content
        if self.template is None:
            raise NotImplementedError("Template is not defined.")
        return self.template.render(
            self, target_language=self.target_language, **environ)
