# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from zope.interface import Invalid
from plone.directives import form
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from plone.namedfile.field import NamedBlobFile



class IInvoiceFolder(form.Schema):

    """An Invoice Folder
    """


class InvoiceFolderView(grok.View):

    """Default view (called "@@view"") for an invoice folder.
    
    The associated template is found in invoice_templates/view.pt.
    """

    grok.context(IInvoiceFolder)
    grok.require('zope2.View')
    #grok.name('view')

    def update(self):
        """Called before rendering the template for this view
        """
        self.haveInvoice = len(self.invoices()) > 0


    @memoize
    def invoices(self):
        """Get all child invoice in this invoice folder.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return [dict(url=invoice.getURL(), invoiceNo=invoice.invoiceNo,) for invoices in
                catalog({'object_provides': IInvoice.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]


class IInvoice(form.Schema):

    """An invoice

        schema = {
            "type" : "object",
            "properties" : {
                "invoiceDescription" : {"type" : "string"},
                "invoiceReferences" : {
                    "type" : "object",
                    "properties": {
                        "userName": {"type": "string"},
                        "displayName" : {"type": "string"},
                    }
                },
                "invoiceDetails" : {
                    "type" : "object",
                    "properties": {
                        "amount": {"type": "string"},
                        "unitprice": {"type": "string"},
                        "total": {"type": "string"},
                        "taxRate": {"type": "string"},
                        "description": {"type": "string"},
                    }
                },
                "senderId" : {"type" : "string"},
                "senderName" : {"type" : "string"},
                "invoiceDate" : {"type" : "string"},
                "invoicePayCondition" : {"type" : "string"},
                "invoiceExpireDate" : {"type" : "string"},
                "invoiceTotalCost" : {"type" : "string"},
                "invoiceCurrency" : {"type" : "string"},
                "invoiceTotalVat" : {"type" : "string"}
            },
        }

    """

    invoiceNo = schema.ASCIILine(title=_(u'Fakturanummer'),
                               description=_(u'Unikt fakturanummer'),
                               required=True)


    invoiceSender = schema.ASCIILine(title=_(u'Avsändare'),
                               description=_(u'Avsändande organisationsnummer'),
                               required=True)

    invoiceSenderName = schema.ASCIILine(title=_(u'Avsändare namn'),
                               description=_(u'Avsändande organisationsnummers namn'),
                               required=False)

    invoiceRecipient = schema.ASCIILine(title=_(u'Mottagare'),
                               description=_(u'Mottagande organisationsnummer'),
                               required=True)

    invoiceRecipientName = schema.ASCIILine(title=_(u'Mottagare namn'),
                               description=_(u'Mottagande organisationsnummers namn'),
                               required=False)

    externalId = schema.ASCIILine(title=_(u'Externt Id'),
                            description=_(u'Fakturans identitet i Megabank'),
                            required=False)

    invoiceDate = schema.Date(title=_(u'Fakturadatum'),
                            description=_(u''),
                            required=False)

    invoicePayCondition = schema.ASCIILine(title=_(u'Betalningsvillkor'),
                            description=_(u''),
                            required=False)

    invoiceExpireDate = schema.Date(title=_(u'Förfallodatum'),
                            description=_(u''),
                            required=False)

    invoiceCurrency = schema.ASCIILine(title=_(u'Valuta'),
                            description=_(u''),
                            required=False)

    invoiceTotalVat = schema.ASCIILine(title=_(u'Total moms'),
                            description=_(u''),
                            required=False)

    invoiceTotalAmount = schema.ASCIILine(title=_(u'Totalt belopp'),
                            description=_(u''),
                            required=False)

    InvoiceAttachment = NamedBlobFile(title=_(u'Faktura'),
                           description=_(u'Fakturafil'),
                           required=False)



class InvoiceView(grok.View):

    """Default view (called "@@view"") for an invoice.
    
    The associated template is found in invoice_templates/view.pt.
    """

    grok.context(IInvoice)
    grok.require('zope2.View')
    #grok.name('view')

    def update(self):
        """Called before rendering the template for this view
        """

