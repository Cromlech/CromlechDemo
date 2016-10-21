# -*- coding: utf-8 -*-

from os import path
from dolmen.template import TALTemplate
from .resources import lite
from cromlech.browser import IView


TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')


def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))


class ITab(IView):
    pass
