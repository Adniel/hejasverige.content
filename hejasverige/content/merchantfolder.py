# -*- coding: utf-8 -*-

from hejasverige.content import _
from plone.memoize.instance import memoize
from plone.app.textfield import RichText
from hejasverige.content.merchant import IMerchant
from Products.CMFCore.utils import getToolByName
from plone.directives import form
from five import grok


class IMerchantFolder(form.Schema):

    """A folder that can contain merchants
    """

    text = RichText(title=_(u'Merchant folder'),
                    description=_(u'A description of the folder'),
                    required=False)


class View(grok.View):

    """Default view (called "@@view"") for a merchant folder.

    The associated template is found in merchantfolder_templates/view.pt.
    """

    grok.context(IMerchantFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        """Called before rendering the template for this view
        """

        self.haveMerchantFolders = len(self.merchantFolders()) > 0
        self.haveMerchant = len(self.merchants()) > 0

    @memoize
    def merchantFolders(self):
        """Get all child merchant folders in this merchant folder.

        We memoize this using @plone.memoize.instance.memoize so that even
        if it is called more than once in a request, the calculations are only
        performed once.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return [dict(url=merchantFolder.getURL(), title=merchantFolder.Title,
                description=merchantFolder.Description) for merchantFolder in
                catalog({'object_provides': IMerchantFolder.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]

    @memoize
    def merchants(self):
        """Get all child merchants in this merchant.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return [dict(url=merchant.getURL(), title=merchant.Title,
                address=merchant.Description) for merchant in
                catalog({'object_provides': IMerchant.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]
