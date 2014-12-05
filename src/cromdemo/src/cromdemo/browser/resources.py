# -*- coding: utf-8 -*-

from fanstatic import Resource, Library, Group
from js.bootstrap import bootstrap_css
from js.jqueryui import jqueryui


Library = Library("lite_resources", 'files')
styles = Resource(Library, 'lite.css', depends=[bootstrap_css])
litejs = Resource(Library, 'jquery.lite.js', depends=[jqueryui])
lite = Group([styles, litejs])
