# -*- coding: utf-8 -*-

from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from zope.interface import Invalid
from hejasverige.content import _
from zope.schema import ValidationError

class ToShortPersonalId(ValidationError):
    "Illegal lenght. Must be 10 digits."

class IllegalCheckDigit(ValidationError):
    "Ogiltig checksiffra"


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
        title=_(u'label_personal_id', default=u'Personal id number'),
        description=_(u'help_personal_id',
                      default=u"We need your personal id number to be able to ensure that you are who you say you are (YYMMDDNNNN)"),
        required=False,
        constraint=validatePersonalId,
        )

    accept = schema.Bool(
        title=_(u'label_accept', default=u'Accept terms of use'),
        description=_(u'help_accept',
                      default=u"Tick this box to indicate that you have found,"
                      " read and accepted the terms of use for this site. "),
        required=True,
        constraint=validateAccept,
        )
