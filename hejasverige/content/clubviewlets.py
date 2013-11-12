# -*- coding: utf-8 -*-

from five import grok
from hejasverige.content.sports import IClub

import logging
logger = logging.getLogger(__name__)

grok.context(IClub)
grok.templatedir("templates")


class ClubViewletManager(grok.ViewletManager):
    """ This viewlet manager is responsible for all hejasverige.megabank viewlet registrations.
        Viewlets are directly referred in templates dir by viewlet name.
    """
    grok.name('hejasverige.content.clubviewletmanager')

# Set viewlet manager default to all following viewlets
grok.viewletmanager(ClubViewletManager)


class InvitationViewlet(grok.Viewlet):
    """ Create a viewlet for invitiations

    """
    grok.name('invitation-viewlet')
    grok.require('hejasverige.InviteMembers')

    def update(self):
        logger.info('Rendered the invitation viewlet')

