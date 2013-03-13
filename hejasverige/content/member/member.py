# -*- coding: utf-8 -*-

import re

from plone.directives import form
from zope import schema
from zope.interface import Invalid, invariant

from hejasverige.content import _
from dexterity.membrane.membrane_helpers import validate_unique_email
from zope.schema import ValidationError


class ToShortPersonalId(ValidationError):
    "Ogiltig längd. 10 siffror."

class IllegalCheckDigit(ValidationError):
    "Ogiltig checksiffra"

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
    raise Invalid(_(u"Not a valid link"))


class IEmail(form.Schema):
    """Email address schema.

    If you have this field, we can make you a member.  To authenticate
    you also need a password though.
    """

    email = schema.TextLine(
        # String with validation in place looking for @, required.
        # Note that a person's email address will be their username.
        title=_(u"E-postadress"),
        required=True,
        constraint=is_email,
    )

    @invariant
    def email_unique(data):
        """The email must be unique, as it is the login name (user name).

        The tricky thing is to make sure editing a user and keeping
        his email the same actually works.
        """
        user = data.__context__
        if user is not None:
            if hasattr(user, 'email') and user.email == data.email:
                # No change, fine.
                return
        error = validate_unique_email(data.email)
        if error:
            raise Invalid(error)


class IMember(IEmail):
    """
    Member
    """

    first_name = schema.TextLine(
        title=_(u"Förnamn"),
        required=True,
        )

    last_name = schema.TextLine(
        title=_(u"Efternamn"),
        required=True,
        )

    personal_id = schema.ASCIILine(
        # url format
        title=_(u"Personnummer"),
        required=True,
        constraint=validatePersonalId,
        )

    form.widget(bio="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    bio = schema.Text(
        title=_(u"Om mig"),
        required=False,
        )
