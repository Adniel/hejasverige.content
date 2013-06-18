# -*- coding: utf-8 -*-

from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from zope.interface import Invalid
from hejasverige.content import _
from zope.schema import ValidationError

#from zope.component import getMultiAdapter

#def getTerms(obj):
#    context_state = getMultiAdapter((obj.context, obj.request),
#                                        name=u'plone_context_state')

#    try: # Plone 4+
#        terms_actions = context_state.actions(category="hejasverige.terms")
#    except TypeError: # Plone 3
#        terms_actions = context_state.actions().get('hejasverige.terms', ())

#    for action in self.mymenu_actions:
#        if action['id'] == 'receivedmessages':
#    return 

class ToShortPersonalId(ValidationError):
    "Illegal lenght. Must be 10 digits."

class IllegalCheckDigit(ValidationError):
    "Ogiltig checksiffra"

class PersonalIdAlreadyRegistered(ValidationError):
    "Det angivna personnumret finns redan. Om du har angivit ditt personnummer och får detta fel, <a href='contactus'>kontakta</a> Heja Sverige"

def personal_id_check_digit(p):
    a,p=[0,2,4,6,8,1,3,5,7,9],[int(i) for i in p]
    return 10-(a[p[0]]+p[1]+a[p[2]]+p[3]+a[p[4]]+p[5]+a[p[6]]+p[7]+a[p[8]])%10


def validateAccept(value):
    if not value:
        return False
    return True

def validatePersonalId(value):
    # check that the personal id conforms to the standard in lenght and that check digit is correct
    if value:
        if len(value) != 10:
            raise ToShortPersonalId(value)
        elif personal_id_check_digit(value) != int(value[9:]):
            # verify that checkdigit is ok
            raise IllegalCheckDigit(value)

    return True

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    personal_id = schema.TextLine(
        title=_(u'label_personal_id', default=u'Personnummer'),
        description=_(u'help_personal_id',
                      default=u"För att identifiera dig behöver vi ditt personnummer (YYMMDDNNNN)"),
        required=False,
        constraint=validatePersonalId,
        )

    kollkoll = schema.Bool(
        title=_(u'label_kollkoll', default=u'Hämta köp automatiskt'),
        description=_(u'help_kollkoll',
                      default=u"Markera detta val för att Heja Sverige ska hämta dina korttransaktioner från vanliga köp. För att Heja Sverige ska kunna göra detta behöver du registrera ditt bankkonto."),
        required=False,
        )

    accept = schema.Bool(
        title=_(u'label_accept', default=u'Acceptera användarvillkor'),
        description=_(u'help_accept',
                      default=u"De finns <a id='commonterms' href='dokument/avtal-och-villkor/avtalsvillkor-medlem/allmanna-villkor'>här</a>"), 
        required=True,
        constraint=validateAccept,
        )
