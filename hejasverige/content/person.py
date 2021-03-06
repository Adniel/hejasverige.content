#-*- coding: utf-8 -*-

import re
import logging
#from plone.indexer import indexer
from plone.indexer.decorator import indexer
from plone.directives import form
from zope import schema
from zope.interface import Invalid, invariant, alsoProvides
from five import grok
from hejasverige.content import _
from AccessControl import Unauthorized
from zope.schema import ValidationError
from zope.interface import Interface
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from sports import IClub, IDistrict, ICouncil
from plone.app.uuid.utils import uuidToObject
from Products.CMFCore.WorkflowCore import WorkflowException
from plone.namedfile.field import NamedBlobImage
from hejasverige.content.interfaces import IMyPages
from zope.component.hooks import getSite
from plone import api

logger = logging.getLogger(__name__)

class ToShortPersonalId(ValidationError):
    "Ogiltig längd. 10 siffror (YYMMDDNNNN)."


class IllegalCheckDigit(ValidationError):
    "Ogiltig checksiffra"

class PersonalIdNotUnique(ValidationError):
    "Det finns redan en person med detta personnummer registrerad som anhörig till dig."

class ThisIsYourOwnPersonalId(ValidationError):
    "Personen har samma personnummer som du själv. Det är inte möjligt."

def get_brains_for_email(context, email, request=None):
    """Anonymous users should be able to look for email addresses.
    Otherwise they cannot log in.

    This searches in the membrane_tool and returns brains with this
    email address.  Hopefully the result is one or zero matches.

    Note that we search for exact_getUserName as the email address is
    supposed to be used a login name (user name).  TODO: We may want
    to change the name of this function to reflect this.
    """
    try:
        email = email.strip()
    except (ValueError, AttributeError):
        return []
    if email == '' or '@' not in email:
        return []

    catalog = getToolByName(context, "portal_catalog", None)

    kw = dict(exact_getUserName=email)
    #args = CatalogSearchArgumentsMap(request, kw)
    #users = user_catalog.search(args)
    users = catalog.unrestrictedSearchResults(**kw)
    return users


def validate_unique_email(email, context=None):
    """Validate this email as unique in the site.
    """
    if context is None:
        context = getSite()
    matches = get_brains_for_email(context, email)
    if not matches:
        # This email is not used yet. Fine.
        return
    if len(matches) > 1:
        msg = "Multiple matches on email %s" % email
        logger.warn(msg)
        return msg
    # Might be this member, being edited.  That should have been
    # caught by our new invariant though, at least when changing the
    # email address through the edit interface instead of a
    # personalize_form.
    match = matches[0]
    try:
        found = match.getObject()
    except (AttributeError, KeyError, Unauthorized):
        # This is suspicious.  Best not to use this one.
        pass
    else:
        if found == context:
            # We are the only match.  Good.
            logger.debug("Only this object itself has email %s", email)
            return

    # There is a match but it is not this member or we cannot get
    # the object.
    msg = "Email %s is already in use." % email
    logger.debug(msg)
    return msg

def get_personal_ids_for_user(context=None):
    if context is None:
        context = getSite()

    mship = getToolByName(context, 'portal_membership')

    home = mship.getHomeFolder()

    catalog = getToolByName(context, "portal_catalog", None)

    personal_ids = [person.personal_id for person in 
                   catalog({'object_provides': IPerson.__identifier__,
                           'path': dict(query='/'.join(home.getPhysicalPath()),), })]


    return personal_ids

def validate_unique_personal_id(personal_id, context=None):
    existing_personal_ids = get_personal_ids_for_user()

    if personal_id in existing_personal_ids:

        return False
    return True

def validate_is_not_own_personal_id(personal_id, context=None):
    current_user = api.user.get_current()
    current_personal_id = current_user.getProperty('personal_id')

    if personal_id == current_personal_id:
        return False
    return True

def personal_id_check_digit(p):
    a,p=[0,2,4,6,8,1,3,5,7,9],[int(i) for i in p]
    return 10-(a[p[0]]+p[1]+a[p[2]]+p[3]+a[p[4]]+p[5]+a[p[6]]+p[7]+a[p[8]])%10

def validatePersonalId(value):
    # check that the personal id conforms to the standard in lenght and that check digit is correct
    if value:
        if len(value) != 10:
            raise ToShortPersonalId(value)
        elif personal_id_check_digit(value) != int(value[9:]):
            # verify that checkdigit is ok
            raise IllegalCheckDigit(value)
    
        # Needs update. You can not edit with this in place since the personal id already exists for the 
        # edited person
        #if not validate_unique_personal_id(value):
        #    raise PersonalIdNotUnique(value)

        if not validate_is_not_own_personal_id(value):
            raise ThisIsYourOwnPersonalId(value)

    return True

def is_email(value):
    """Is this an email address?
    """
    if not isinstance(value, basestring) or not '@' in value:
        raise Invalid(_(u"Ogiltig epostadress"))
    return True

def is_url(value):
    """Is this a URL?
    """
    if isinstance(value, basestring):
        pattern = re.compile(r"^https?://[^\s\r\n]+")
        if pattern.search(value.strip()):
            return True
    raise Invalid(_(u"Ogiltig länk"))


class IEmail(form.Schema):
    """Email address schema.
    """

    email = schema.TextLine(
        # String with validation in place looking for @, required.
        # Note that a person's email address will be their username.
        title=_(u"E-postadress"),
        required=False,
        constraint=is_email,
    )

    #@invariant
    #def email_unique(data):
    #    """The email must be unique, as it is the login name for a user.

    #    The tricky thing is to make sure editing a user and keeping
    #    his email the same actually works.
    #    """
    #    user = data.__context__
    #    if user is not None:
    #        if hasattr(user, 'email') and user.email == data.email:
                # No change, fine.
    #            return
    #    error = validate_unique_email(data.email)
    #    if error:
    #        raise Invalid(error)


#class IPerson(IEmail):
class IPerson(form.Schema):
    """ A person object filed for a user 
    """

    first_name = schema.TextLine(
        title=_(u"Förnamn"),
        required=True,
        )

    last_name = schema.TextLine(
        title=_(u"Efternamn"),
        required=True,
        )

    #homepage = schema.TextLine(
        # url format
    #    title=_(u"Extern Hemsida"),
    #    required=False,
    #    constraint=is_url,
    #    )

    personal_id = schema.ASCIILine(
        title=_(u"Personnummer (ÅÅMMDDNNNN)"),
        required=True,
        constraint=validatePersonalId,
        )

    avatar = NamedBlobImage(title=_(u'Bild'),
                           description=_(u'Ladda upp en bild på personen'
                           ), required=False)

    #form.widget(bio="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    #bio = schema.Text(
    #    title=_(u"Om personen"),
    #    required=False,
    #    )

class IRelationFolder(form.Schema):
    """ A relation folder used to contain relations in 
        users personal folders
    """


class IRelation(form.Schema):
    """ A relation object filed under a person
    """

    foreign_id = schema.ASCIILine(
        title=_(u"Främmande id"),
        required=True,
        )


# Dexterity behaviour to get the object name (title) from fullname
from plone.app.content.interfaces import INameFromTitle
from zope.component import adapts
from zope.interface import implements


def get_full_name(context):
    names = [
        context.first_name,
        context.last_name,
        ]
    return u' '.join([name for name in names if name])


class INameFromFullName(INameFromTitle):
    """Get the name from the full name.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class NameFromFullName(object):
    implements(INameFromFullName)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return get_full_name(self.context)


@indexer(IPerson)
def Title(object, **kw):
    #import pdb; pdb.set_trace()
    name = INameFromFullName(object, None)
    if name is None:
        name = NameFromFullName(object)
        #print 'name was None...'
    #print 'Nu händer det...', name
    #print 'Objekt:', str(object)
    if name is not None:
        return name.title
    return object.Title()

# End behaviour


# Views
from plone.dexterity.utils import createContent
from plone.dexterity.utils import addContentToContainer
from plone.uuid.interfaces import IUUID
class ShowAddRelationForm(grok.View):
    """
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('add-relation2')
    grok.implements(IMyPages)

    def add_relation(self, id, member_type='supporter'):
        relobj = createContent(portal_type='hejasverige.relation',
                                 foreign_id=id,
                                )

        try:
            item = addContentToContainer(container=self.__parent__, object=relobj, checkConstraints=False)
        except Exception, ex:
            err = 'Unable to add relation with id', id, 'to', str(self.__parent__), 'due to', str(ex)
            print err
            #log(err)
            return None
        else:
            # Push to correct state depending on type
            workflowTool = getToolByName(item, 'portal_workflow')
            if member_type == 'member':
                transition = 'pend'
            else:
                transition = 'support'

            try:
                workflowTool.doActionFor(item, transition, comment='')
                print "Object", item.id, "changed state"
            except WorkflowException:
                print "Could not apply workflow transition", transition, ".", item.id, "state not changed"

        return item


    def districts(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        return  [dict(name=district.Title, value=district.id)
                for district in
                catalog({'object_provides': IDistrict.__identifier__,
                'sort_on': 'sortable_title'})]


    def councils(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        query_dict = {'object_provides': ICouncil.__identifier__,
                      'sort_on': 'sortable_title'
                     }
        if self.selectedDistrictPath:
            query_dict['path'] = dict(query=self.selectedDistrictPath)
        
            return  [dict(name=council.Title, value=council.id)
                    for council in
                    catalog(query_dict)]

    def sports(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        #import pdb; pdb.set_trace()

        #uniqueValuesFor        
        return [{'name': 'Dart', 'value':'Dart'},{'name': 'Fotboll', 'value': 'Fotboll'}]

    def update(self):
        self.add_club = self.request.form.get('add-club') or None
        if self.add_club:
            member_type = self.request.form.get('type') or 'supporter'
            print 'Member type:', member_type
            # add a new relation object. Then redirect to my-person
            self.add_relation(self.add_club, member_type=member_type)
            self.redirect(self.url('my-person'))

        # check if form submitted and return correct view
        

        self.request.set('disable_border', True)
        self.selectedDistrict = self.request.form.get('district') or None
        self.selectedDistrictPath = None
        self.selectedCouncil = self.request.form.get('council') or None
        self.selectedCouncilPath = None

        self.selectedSport = self.request.form.get('sport') or None

        catalog = getToolByName(self.context, 'portal_catalog')
        if self.selectedDistrict:
            # get the path to the selected district
            selectedDistrictBrains = catalog({'object_provides': IDistrict.__identifier__, 'id': self.selectedDistrict})
            if len(selectedDistrictBrains) > 0:
                self.selectedDistrictPath = selectedDistrictBrains[0].getPath()

        if self.selectedCouncil:
            # get the path to the selected district
            selectedCouncilBrains = catalog({'object_provides': ICouncil.__identifier__, 'id': self.selectedCouncil})
            if len(selectedCouncilBrains) > 0:
                self.selectedCouncilPath = selectedCouncilBrains[0].getPath()



class AddRelation(grok.View):
    """
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('add-relation')
    grok.implements(IMyPages)

    def getUID(self):
        """ AT and Dexterity compatible way to extract UID from a content item """
        context = self.context.aq_base
        uuid = IUUID(context, None)
        return uuid    

    def add_relation(self, id, member_type='supporter'):
        relobj = createContent(portal_type='hejasverige.relation',
                                 foreign_id=id,
                                )

        #import pdb; pdb.set_trace()

        try:
            item = addContentToContainer(container=self.__parent__, object=relobj, checkConstraints=False)
        except Exception, ex:
            err = 'Unable to add relation with id', id, 'to', str(self.__parent__), 'due to', str(ex)
            print err
            #log(err)
            return None
        else:
            # Push to correct state depending on type
            workflowTool = getToolByName(item, 'portal_workflow')
            if member_type == 'member':
                transition = 'pend'
            else:
                transition = 'support'

            try:
                workflowTool.doActionFor(item, transition, comment='')
                print "Object", item.id, "changed state"
            except WorkflowException:
                print "Could not apply workflow transition", transition, ".", item.id, "state not changed"

        return item


    def update(self):
        
        #import pdb; pdb.set_trace()
        #alsoProvides(self, IMyPages)
        #return_view should be either my-person or add-club
        self.add_club = self.request.form.get('add-club') or None
        self.wizard = self.request.form.get('wizard') or None
        
        if self.add_club:
            self.return_view = self.request.form.get('return_view') or 'add-club'
            member_type = self.request.form.get('type') or 'supporter'
            print 'Member type:', member_type
            # add a new relation object. Then redirect to my-person
            self.add_relation(self.add_club, member_type=member_type)

            #self.redirect(self.url('my-person'))
            #import pdb; pdb.set_trace()
            if self.wizard == 'true':
                self.redirect(self.return_view)
            else:
                self.redirect(self.url(self.return_view))
        else:
            if self.wizard == 'true':
                self.return_view = self.request.get('wizard_url')
            elif self._BrowserView__getParent().Type() == 'Person':
                self.return_view = 'my-person'
            else:
                self.return_view = 'my-clubs'

        self.request.set('disable_border', True)
        self.selectedDistrict = self.request.form.get('district') or None
        self.selectedDistrictPath = None
        self.selectedCouncil = self.request.form.get('council') or None
        self.selectedCouncilPath = None

        self.selectedSport = self.request.form.get('sport') or None

        catalog = getToolByName(self.context, 'portal_catalog')
        if self.selectedDistrict:
            # get the path to the selected district
            selectedDistrictBrains = catalog({'object_provides': IDistrict.__identifier__, 'id': self.selectedDistrict})
            if len(selectedDistrictBrains) > 0:
                self.selectedDistrictPath = selectedDistrictBrains[0].getPath()

        if self.selectedCouncil:
            # get the path to the selected district
            selectedCouncilBrains = catalog({'object_provides': ICouncil.__identifier__, 'id': self.selectedCouncil})
            if len(selectedCouncilBrains) > 0:
                self.selectedCouncilPath = selectedCouncilBrains[0].getPath()


    @memoize
    def clubs(self, start=0, size=20):
        """Get all child clubs within this filter.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        retu = None

        # If a council is selected, use the more specifict council path to restrict
        # result set
        if self.selectedCouncilPath:
            query_path = self.selectedCouncilPath
        else:
            query_path = self.selectedDistrictPath

        if self.selectedDistrictPath:
            retu =  [dict(uid=club.UID, id=club.id, url=club.getURL(), title=club.Title, sport=club.Sport,
                    address=club.Description) for club in
                    catalog({'object_provides': IClub.__identifier__,
                    'path': dict(query=query_path),
                    'sort_on': 'sortable_title'})]                    
        else:
            retu =  [dict(uid=club.UID, id=club.id, url=club.getURL(), title=club.Title, sport=club.Sport,
                    address=club.Description) for club in
                    catalog({'object_provides': IClub.__identifier__,
                    'sort_on': 'sortable_title'})]        

        #import pdb; pdb.set_trace()

        return retu

    def districts(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        return  [dict(name=district.Title, value=district.id)
                for district in
                catalog({'object_provides': IDistrict.__identifier__,
                'sort_on': 'sortable_title'})]

    def councils(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        query_dict = {'object_provides': ICouncil.__identifier__,
                      'sort_on': 'sortable_title'
                     }
        if self.selectedDistrictPath:
            query_dict['path'] = dict(query=self.selectedDistrictPath)
        
            return  [dict(name=council.Title, value=council.id)
                    for council in
                    catalog(query_dict)]

        #if self.selectedDistrictPath:
        #    return  [dict(name=council.Title, value=council.id)
        #                for council in
        #                catalog({'object_provides': ICouncil.__identifier__,
        #                'path': dict(query=self.selectedDistrictPath),
        #                'sort_on': 'sortable_title'})]
        #else:
        #    return  [dict(name=council.Title, value=council.id)
        #            for council in
        #            catalog({'object_provides': ICouncil.__identifier__,
        #            'sort_on': 'sortable_title'})]

    def sports(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        #import pdb; pdb.set_trace()

        #uniqueValuesFor        
        return [{'name': 'Dart', 'value':'Dart'},{'name': 'Fotboll', 'value': 'Fotboll'}]

class AbortRelationView(grok.View):
    grok.context(IRelation)
    grok.require('zope2.View')
    grok.name('abort')
    grok.template('abortrelation')

    def update(self):
        #import pdb; pdb.set_trace()
        button_ok = self.request.form.get('form.button.Ok') or None
        if button_ok:
            workflowTool = getToolByName(self.context, 'portal_workflow')
            try:
                workflowTool.doActionFor(self.__parent__, 'abort', comment='')
            except WorkflowException, ex:
                print "Could not apply workflow transition 'abort'.", self.__parent__.UID(), "with foreign_id", self.__parent__.foreign_id,"state not changed.", ex

            if self._BrowserView__getParent().__parent__.Type() == 'Person':
                return_view = 'my-person'
            else:
                return_view = 'my-clubs'

            self.redirect(self.url(return_view))
        else:
            self.title = uuidToObject(self.context.foreign_id).Title()
            if self.__parent__.__parent__.Type() == 'Person':
                self.remove_from = self.__parent__.__parent__.first_name + ' ' + self.__parent__.__parent__.last_name
            else:
                self.remove_from = _(u'dig själv')

# temp view for reindexing brains
from Products.CMFCore.interfaces import ISiteRoot
class ReindexBrains(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('reindexbrains')

    def render(self):

        interface = self.request.form.get('if') or None

        catalog = getToolByName(self.context, 'portal_catalog')

        query_dict = {}
        result = []
        result.append("Reindexed objects")

        if interface:
            mod = getattr(self.module_info.getModule(), interface)
            query_dict['object_provides'] = mod.__identifier__
            result.append("for interface " + query_dict['object_provides'])
        
        brains = catalog(query_dict)
        #import pdb;pdb.set_trace()
        for brain in brains:
            res = catalog.reindexObject(brain.getObject())
            result.append(str(brain) + " reindexed")
        return result


class MyPerson(grok.View):
    """View (called "@@my-person"") for a family.

    The associated template is found in person_templates/myperson.pt.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('my-person')
    grok.implements(IMyPages)

    def update(self):
        """Called before rendering the template for this view
        """
        #import pdb; pdb.set_trace()
        self.request.set('disable_border', True)

    @memoize
    def members(self):
        """Get all relations bound to the current person.
        """

        catalog = getToolByName(self.context, 'portal_catalog')
        portal_workflow = getToolByName(self.context, "portal_workflow")

        # import pdb;pdb.set_trace()

        # # # # # # # #
        # retrieve member relations
        # # # # # # # #
        retu = catalog({'object_provides': IRelation.__identifier__,
               'review_state': ('pending', 'approved'),
               'path': dict(query='/'.join(self.context.getPhysicalPath()),
               depth=1), 'sort_on': 'sortable_title',})

        # Should really be added as a Title field index on the relation type, 
        # but that can be done later. For now, just list the containing objects.
        # needs to also provide review_state
        member_objs = [uuidToObject(brain.getObject().foreign_id) for brain in retu]

        # remove empty references (if strange ids is by some reason added). (otherwise None values instead of club objects
        # is inside the list)
        member_objs = [x for x in member_objs if x]

        #return member_objs

        clubs = [dict(clubobj=uuidToObject(relation.getObject().foreign_id),
                relation=relation, portal_type=relation.getObject().aq_inner.aq_parent.portal_type, 
                parentobj=relation.getObject().aq_inner.aq_parent, 
                status=portal_workflow.getStatusOf("hejasverige_relation_workflow", relation.getObject())['review_state'])
                for relation in
                catalog({'object_provides': IRelation.__identifier__,
                'review_state': ('pending', 'approved'),                    
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title',})]

        return clubs


    @memoize
    def supporters(self):
        """Get all relations bound to the current person.
        """

        catalog = getToolByName(self.context, 'portal_catalog')
        #import pdb;pdb.set_trace()

        # # # # # # # #
        # retrieve supporter relations
        # # # # # # # #
        retu = catalog({'object_provides': IRelation.__identifier__,
               'review_state': 'supporter',
               'path': dict(query='/'.join(self.context.getPhysicalPath()),
               depth=1), 'sort_on': 'sortable_title',})

        # Should really be added as a Title field index on the relation type, 
        # but that can be done later. For now, just list the containing objects.
        supporter_objs = [uuidToObject(brain.getObject().foreign_id) for brain in retu]

        # remove empty references (if strange ids is by some reason added). (otherwise None values instead of club objects
        # is inside the list)
        supporter_objs = [x for x in supporter_objs if x]

        return supporter_objs



class MyFamily1(grok.View):
    """View (called "@@my-family"") for a family.

    The associated template is found in person_templates/myfamily.pt.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('my-family1')
    grok.implements(IMyPages)
    #grok.template('myfamily')

    def update(self):
        """Called before rendering the template for this view
        """
        self.request.set('disable_border', True)
        self.codes = ()

    @memoize
    def persons(self, start=0, size=11):
        """Get all persons in this folder.
        """

        catalog = getToolByName(self.context, 'portal_catalog')

        retu = [dict(url=person.getURL(), name=person.Title,
               personal_id=person.personal_id) for person in 
               catalog({'object_provides': IPerson.__identifier__,
               'path': dict(query='/'.join(self.context.getPhysicalPath()),
               depth=1), 'sort_on': 'sortable_title', 'b_start': start,
               'b_size': size,})]

        return retu


class MyFamily(grok.View):
    """View (called "@@my-family"") for a family.

    The associated template is found in person_templates/myfamily.pt.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('my-family')
    grok.implements(IMyPages)
    #grok.template('myfamily')

    def update(self):
        """Called before rendering the template for this view
        """
        self.request.set('disable_border', True)
        self.codes = ()

    @memoize
    def persons(self, start=0, size=11):
        """Get all persons in this folder.
        """

        catalog = getToolByName(self.context, 'portal_catalog')
        #import pdb; pdb.set_trace()
        #family = [dict(url=person.getURL(), name=person.Title,
        #          personal_id=person.personal_id) for person in 
        family =  catalog({'object_provides': IPerson.__identifier__,
                  'path': dict(query='/'.join(self.context.getPhysicalPath()),
                  depth=1), 'sort_on': 'sortable_title', 'b_start': start,
                  'b_size': size,})# ]

        family_objs = [brain.getObject() for brain in family]

        from plone.app.uuid.utils import uuidToObject
        persons =[]

        for item in family_objs:
            clubs = [uuidToObject(relation.getObject().foreign_id) 
                    for relation in
                    catalog({'object_provides': IRelation.__identifier__,
                    'review_state': ('pending', 'approved'),                                                                
                    'path': dict(query='/'.join(item.getPhysicalPath()),
                    depth=1),'sort_on': 'sortable_title'})]

            clubs = [x for x in clubs if x]
            persons.append({'name': item.first_name + ' ' + item.last_name, 
                            'clubs': clubs, 
                            'person': item})

        return persons





class MyClubs(grok.View):
    """View (called "@@my-clubs"") for a family.

    The associated template is found in person_templates/myclubs.pt.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('my-clubs')
    grok.implements(IMyPages)

    @memoize
    def clubs(self, start=0, size=11):
        """Get all clubs related to a person.
        """
        mship = getToolByName(self.context, 'portal_membership')

        home = mship.getHomeFolder()

        catalog = getToolByName(self.context, 'portal_catalog')

        portal_workflow = getToolByName(self.context, "portal_workflow")
        
        clubs = [dict(clubobj=uuidToObject(relation.getObject().foreign_id),
                relation=relation, portal_type=relation.getObject().aq_inner.aq_parent.portal_type, 
                parentobj=relation.getObject().aq_inner.aq_parent, 
                status=portal_workflow.getStatusOf("hejasverige_relation_workflow", relation.getObject())['review_state'])
                for relation in
                catalog({'object_provides': IRelation.__identifier__,
                'review_state': ('pending', 'approved'),                                        
                'path': dict(query='/'.join(home.getPhysicalPath()),),
                'sort_on': 'sortable_title'})]

        clubs = [x for x in clubs if x['clubobj']]
        # for j in [i for i in dir(clubs[0].get('relation').getObject().aq_inner.aq_parent) if i.startswith('p')]: print j
        # clubs[0].get('relation').getObject().aq_inner.aq_parent.portal_type = 'hejasverige.person'
        return clubs

    def update(self):
        """Called before rendering the template for this view
        """
        self.request.set('disable_border', True)

    #def render(self):
        """Get all clubs related to a person.
        """
        mship = getToolByName(self.context, 'portal_membership')

        home = mship.getHomeFolder()

        catalog = getToolByName(self.context, 'portal_catalog')

        portal_workflow = getToolByName(self.context, "portal_workflow")

        clubs = [dict(clubobj=uuidToObject(relation.getObject().foreign_id),
                relation=relation, portal_type=relation.getObject().aq_inner.aq_parent.portal_type, 
                parentobj=relation.getObject().aq_inner.aq_parent, 
                status=portal_workflow.getStatusOf("hejasverige_relation_workflow", relation.getObject())['review_state'])
                for relation in
                catalog({'object_provides': IRelation.__identifier__,
                'path': dict(query='/'.join(home.getPhysicalPath()),),
                'sort_on': 'sortable_title'})]

        
