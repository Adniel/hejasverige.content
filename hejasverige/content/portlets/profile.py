"""Define a portlet used to show the user profile. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
"""

#import random
from plone import api

#from zope import schema
from zope.formlib import form
from zope.interface import implements
#from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
#from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

#from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

#from hejasverige.content.profile import IProfile
from hejasverige.content import _
from hejasverige.content.person import IPerson
from hejasverige.content.person import IRelation

from hejasverige.content.interfaces import IMyPages
# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class IProfilePortlet(IPortletDataProvider):
    """ Nothing to configure for this portlet
    """

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(IProfilePortlet)

    def __init__(self):
        """ init the configuration here if any
            self.field = parameterfield
        """        

    title = _(u"Min profil")

# -*- coding: utf-8 -*-

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('profile.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown.

    @property
    def available(self):
        #import pdb; pdb.set_trace()
        #return True
        return IMyPages.providedBy(self.__parent__)


    def portletfield(self):
        return "Min portlet"

    def megabankisinstalled(self):
        try:
            from hejasverige.megabank.bank import Bank 
            print 'Megabank is installed'
            return True
        except:
            print 'Megabank is not installed'
            return False

    def myinfo(self):
        user = api.user.get_current()
        fullname = user.getProperty('fullname')
        if type(fullname).__name__ == 'object':
            fullname = None

        portrait = user.portal_memberdata.getPersonalPortrait()

        #import pdb;pdb.set_trace()
        info = {'name': fullname, 
                'clubs': ['BB', 'CC', 'DD'], 
                'portrait': portrait}



        if self.megabankisinstalled:
            from hejasverige.megabank.bank import Bank
            pid = api.user.get_current().getProperty('personal_id')

            # if field is not defined as a personal property it becomes an object and the bank fails to load
            if type(pid).__name__ == 'object':
                info['balance'] = 'error'
                info['amount_pending'] = 'error'
            else:
                import locale
                locale.setlocale(locale.LC_ALL, 'sv_SE.utf-8')
                try:
                    accountinfo = Bank().getAccount(personalid=pid, context=self)
                    info['balance'] = locale.currency(accountinfo.get('Balance', None), grouping=True)
                    info['amount_pending'] = locale.currency(accountinfo.get('AmountPending', None), grouping=True)
                except:
                    info['balance'] = 'conerror'
                    info['amount_pending'] = 'conerror'

        #import pdb; pdb.set_trace()
        return info        
    
    def myfamily(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        mship = getToolByName(self.context, 'portal_membership')

        home = mship.getHomeFolder()
        #import pdb; pdb.set_trace()
        #family = [dict(name=person.Title, value=person.id)
        #         for person in
        family = catalog({'object_provides': IPerson.__identifier__,
                'path': dict(query='/'.join(home.getPhysicalPath())), 
                'sort_on': 'sortable_title'})

        family_objs = [brain.getObject() for brain in family]

        from plone.app.uuid.utils import uuidToObject
        persons =[]

        for item in family_objs:
            clubs = [uuidToObject(relation.getObject().foreign_id) 
                    for relation in
                    catalog({'object_provides': IRelation.__identifier__,
                    'path': dict(query='/'.join(item.getPhysicalPath()),
                    depth=1),'sort_on': 'sortable_title'})]

            clubs = [x for x in clubs if x]
            persons.append({'name': item.first_name + ' ' + item.last_name, 
                            'clubs': clubs, 
                            'person': item})


        #family = [{'name': 'Anna Berg', 
        #           'clubs': ['FBK', 'KBK'], 
        #           'portrait': 'http://www.realtid.se/ArticlePages/200909/18/20090918143058_Realtid261/Roth_von_Ulf2_IBL_200.jpg'},
        #          {'name': 'Anne Borg', 
        #           'clubs': ['SKTF', 'LRF'], 
        #           'portrait': 'http://www.fubiz.net/wp-content/uploads/2011/08/martin-schoeller-iggy-pop-portrait-550x687.jpg'}
        #         ]

        return persons
# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.AddForm):
    form_fields = form.Fields(IProfilePortlet)
    label = _(u"Add Profile portlet")
    description = _(u"This portlet displays the profile for the current user.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IProfilePortlet)
    label = _(u"Edit Profile portlet")
    description = _(u"This portlet displays the current user profile.")
