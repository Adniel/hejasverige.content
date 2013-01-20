# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from zope.interface import Invalid
from plone.directives import form
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from hejasverige.content.pos import IPos


class IStore(form.Schema):

    """A Store
...."""

    storeId = schema.ASCIILine(title=_(u'Store Id'),
                               description=_(u'The id defining the store'))


class View(grok.View):

    """Default view (called "@@view"") for a store.
    
    The associated template is found in store_templates/view.pt.
    """

    grok.context(IStore)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        """Called before rendering the template for this view
        """
        self.havePos = len(self.pos()) > 0

    @memoize
    def pos(self):
        """Get all child poses in this store.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        poslist = [dict(url=pos.getURL(), title=pos.Title,
                   address=pos.Description) for pos in
                   catalog({'object_provides': IPos.__identifier__,
                   'path': dict(query='/'.join(self.context.getPhysicalPath()),
                   depth=1), 'sort_on': 'sortable_title'})]

        print poslist
        return poslist
