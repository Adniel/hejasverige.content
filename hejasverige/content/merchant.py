# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from zope.interface import Invalid
from plone.directives import form, dexterity
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

def discountIsValid(value):
    """
    """
    if(value):
        try:
            value = float(value)
            if value>100:
                raise Invalid(_(u'Discount to large. Discount must be less than 100 and greater than 0.'))
            if value<0:
                raise Invalid(_(u'Discount to small. Discount must be less than 100 and greater than 0.'))
        except:
            raise Invalid(_(u'The discount must be numeric'))
    return True

def transaction_feeIsValid(value):
    """
    """
    if(value):
        try:
            value = float(value)
            if value<0:
                raise Invalid(_(u'Transaction fee to small. Fee must be less than greater than 0.'))
        except:
            raise Invalid(_(u'The transaction_fee must be numeric'))
    return True

class IMerchant(form.Schema):

    """A Merchant
	"""

    corporateId = schema.ASCIILine(title=_(u'Corporate Id'), 
                                   description=_(u'The VAT number defining the merchant'),
                                   constraint=corporateIdIsValid)

    customerId = schema.ASCIILine(title=_(u'Customer Id'), 
                                  description=_(u'A number defining the merchant as a customer'),
                                  required=False,)

    supplierId = schema.ASCIILine(title=_(u'Supplier Id'), 
                                  description=_(u'A number defining the merchant as a supplier'),
                                  required=False,)

    discount = schema.ASCIILine(title=_(u'Discount'), 
                                description=_(u'The merchant´s agreed discount for Heja Sverige members'),
                                required=False,
                                constraint=discountIsValid)

    transaction_fee = schema.ASCIILine(title=_(u'Transaction Fee'), 
                                description=_(u'The merchant´s agreed transaction fee'),
                                required=False,
                                constraint=transaction_feeIsValid)

    dexterity.read_permission(transaction_description='cmf.AddPortalContent') 
    dexterity.write_permission(transaction_description='cmf.ManagePortal') 
    transaction_description = schema.List(value_type=schema.TextLine(),
                                          title=_(u'Transaction Description'), 
                                          description=_(u'Regular expressions used to evaulate transaction descriptions from external systems. One expression per line.'),
                                          required=False)


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
    	
