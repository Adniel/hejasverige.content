# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from hejasverige.content import _
from hejasverige.member.member import IMember
from zope.interface import Invalid
from plone.directives import form
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from plone.app.textfield import RichText

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope.interface import alsoProvides

grok.templatedir('templates')


## # # # # # # # # # #
# The district folder
## # # # # # # # # # #

class IDistrictFolder(form.Schema):

    """A folder that can contain districts
    """

    text = RichText(title=_(u'Distriktfolder'),
                    description=_(u'A description of the folder'),
                    required=False)


class DistrictFolderView(grok.View):

    """Default view (called "@@view"") for a merchant folder.

    The associated template is found in templates/districtfolder.pt.
    """

    grok.context(IDistrictFolder)
    grok.require('zope2.View')
    grok.name('view')
    grok.template('districtfolder')

    def update(self):
        """Called before rendering the template for this view
        """
        self.haveDistrict = len(self.districts()) > 0

    @memoize
    def districts(self):
        """Get all child districts in this folder.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        d = [dict(url=district.getURL(), title=district.Title,
             address=district.Description) for district in
             catalog({'object_provides': IDistrict.__identifier__,
             'path': dict(query='/'.join(self.context.getPhysicalPath()),
             depth=1), 'sort_on': 'sortable_title'})]
        print d
        return d


## # # # # # # #
# The district
## # # # # # # #

def districtIdIsValid(value):
    # Verify uniqueness, please...
    if value:
        if 1 == 2:
            raise Invalid(_(u'The districtId is invalid'))
    return True


class IDistrict(form.Schema):

    """A District
    """

    districtId = schema.ASCIILine(title=_(u'District Id'),
                                  description=_(u'An external id identifying the district'
                                  ), constraint=districtIdIsValid)


class DistrictView(grok.View):

    """Default view (called "@@view"") for a district.

    The associated template is found in templates/district.pt.
    """

    grok.context(IDistrict)
    grok.require('zope2.View')
    grok.name('view')
    grok.template('district')

    def update(self):
        """Called before rendering the template for this view
        """
        self.haveCouncil = len(self.councils()) > 0

    @memoize
    def councils(self):
        """Get all child councils for this district.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return [dict(url=council.getURL(), title=council.Title,
                address=council.Description) for council in
                catalog({'object_provides': ICouncil.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]


## # # # # # # #
# The council
## # # # # # # #

def councilIdIsValid(value):
    # Verify uniqueness, please...
    if value:
        if 1 == 2:
            raise Invalid(_(u'The councilId is invalid'))
    return True


class ICouncil(form.Schema):

    """A Council
    """

    councilId = schema.ASCIILine(title=_(u'Council Id'),
                                 description=_(u'An external id identifying the council'
                                 ), constraint=councilIdIsValid)


class CouncilView(grok.View):

    """Default view (called "@@view"") for a council.

    The associated template is found in templates/council.pt.
    """

    grok.context(ICouncil)
    grok.require('zope2.View')
    grok.name('view')
    grok.template('council')

    def update(self):
        """Called before rendering the template for this view
        """
        self.haveClub = len(self.clubs()) > 0

    @memoize
    def clubs(self):
        """Get all child clubs in this council.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return [dict(url=club.getURL(), title=club.Title, sport=club.Sport,
                address=club.Description) for club in
                catalog({'object_provides': IClub.__identifier__,
                'path': dict(query='/'.join(self.context.getPhysicalPath()),
                depth=1), 'sort_on': 'sortable_title'})]


## # # # # # # #
# The club
## # # # # # # #

def clubIdIsValid(value):
    # Verify uniqueness, please...
    if value:
        if 1 == 2:
            raise Invalid(_(u'The clubId is invalid'))
    return True


class IClub(form.Schema, IImageScaleTraversable):

    """A Club
    """

    clubId = schema.ASCIILine(title=_(u'Club Id'),
                              description=_(u'An external id identifying the club'
                              ), constraint=clubIdIsValid)

    Sport = schema.TextLine(title=_(u'Sport'),
                            description=_(u'The main sport for the club'),
                            required=False)

    ExternalUrl = schema.TextLine(title=_(u'External Url'),
                                  description=_(u'Url to the web page for the club'
                                  ), required=False)

    #
    Badge = NamedBlobImage(title=_(u'Emblem'),
                           description=_(u'Upload an image used as badge for the specified club'
                           ), required=False)

    Founded = schema.TextLine(title=_(u'Grundad'),
                              description=_(u'The point in time when the club was founded'
                              ), required=False)

    IdrottOnlineId = schema.ASCIILine(title=_(u'Idrottonlineid'),
                                      description=_(u'The club id used at idrottonline'
                                      ), required=False)

    Address1 = schema.TextLine(title=_(u'Adress 2'), description=_(u''),
                               required=False)

    Address2 = schema.TextLine(title=_(u'Adress 1'), description=_(u''),
                               required=False)

    City = schema.TextLine(title=_(u'Stad'), description=_(u''),
                           required=False)

    PostalCode = schema.TextLine(title=_(u'Postnummer'), description=_(u''),
                                 required=False)

    Phone = schema.TextLine(title=_(u'Telefon'), description=_(u''),
                            required=False)

    Email = schema.TextLine(title=_(u'Epost'), description=_(u''),
                            required=False)

    VatNo = schema.TextLine(title=_(u'Vat No'), description=_(u''),
                            required=False)

    BankGiro = schema.TextLine(title=_(u'Bankgiro'), description=_(u''),
                               required=False)

    PlusGiro = schema.TextLine(title=_(u'Plusgiro'), description=_(u''),
                               required=False)

    Presentation = RichText(title=_(u'Presentation'), description=_(u''),
                            required=False)

    form.fieldset('members',
            label=u"Medlemmar",
            fields=['ordinaryMembers', 'economyMembers']
        )

    # Use invariant to make sure members only exists in one group, or make them not appear in members
    # group if they are in economy
    ordinaryMembers = RelationList(
        title=u"Medlemmar",
        default=[],
        value_type=RelationChoice(title=_(u"Medlemmar"),
                                  source=ObjPathSourceBinder(object_provides=IMember.__identifier__)),
        required=False,
    )

    # tactical comment
    economyMembers = RelationList(
        title=u"Ekonomiansvariga",
        default=[],
        value_type=RelationChoice(title=_(u"Ekonomiansvariga"),
                                  source=ObjPathSourceBinder(object_provides=IMember.__identifier__)),
        required=False,
    )



class ClubView(grok.View):

    """Default view (called "@@view"") for a club.
    
    The associated template is found in templates/club.pt.
    """

    grok.context(IClub)
    grok.require('zope2.View')
    grok.name('view2')
    grok.template('club')

    def update(self):
        """Called before rendering the template for this view
        """
