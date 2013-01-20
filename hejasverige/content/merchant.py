# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from zope.interface import Invalid
from plone.directives import form
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from hejasverige.content.store import IStore

def corporateIdIsValid(value):
    """Constraint function to make sure a given corporateId is corporateIdIsValid
	   TODO: Check the number to ensure the corretct format also
	"""
    if value:
        if len(value) != 10:
            raise Invalid(_(u'The corporateId must be 10 digits'))
    return True


class IMerchant(form.Schema):

    """A Merchant
	"""

    corporateId = schema.ASCIILine(title=_(u'Corporate Id'), description=_(u'The VAT number defining the merchant'),
                                   constraint=corporateIdIsValid)

    customerId = schema.ASCIILine(title=_(u'Customer Id'), description=_(u'A number defining the merchant as a customer'))

    supplierId = schema.ASCIILine(title=_(u'Supplier Id'), description=_(u'A number defining the merchant as a supplier'))

class View(grok.View):

    """Default view (called "@@view"") for a merchant.
    
    The associated template is found in merchant_templates/view.pt.
    """

    grok.context(IMerchant)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.haveStores = len(self.stores()) > 0

    @memoize
    def stores(self):
        """Get all child stores in this merchant.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return [dict(url=store.getURL(), title=store.Title,
                address=store.Description) for store in
                catalog({'object_provides': IStore.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]
    	
