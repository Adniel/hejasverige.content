# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from zope.interface import Invalid
from plone.directives import form


class IPos(form.Schema):

    """A Pos
	"""

    posId = schema.ASCIILine(title=_(u'Pos Id'), description=_(u'The serial number defining a point of sale'))


class View(grok.View):

    """Default view (called "@@view"") for a pos.
    
    The associated template is found in pos_templates/view.pt.
    """

    grok.context(IPos)
    grok.require('zope2.View')
    grok.name('view')

    #def render(self):
    #    """Called before rendering the template for this view
    #    """
    	
