# -*- coding: utf-8 -*-

from . import tal_template
from .layout import ProtectedHeader
from ..models import ILeaf

from dolmen.forms.base import name, context, form_component
from dolmen.forms.base import Fields, Form
from dolmen.view import make_layout_response
from cromlech.webob.response import Response


@form_component
@name('edit')
@context(ILeaf)
class Edit(Form):
    responseFactory = Response
    make_response = make_layout_response
    fields = Fields(ILeaf)
