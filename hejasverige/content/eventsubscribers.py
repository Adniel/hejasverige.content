from five import grok
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from AccessControl.SecurityManagement import newSecurityManager

import logging
logger = logging.getLogger(__name__)

@grok.subscribe(IUserLoggedInEvent)
def createUserFolders(event):
    """ creates default-folders for the user
    """
    print event.principal, "has logged in"

    try:
        inst = getToolByName(event.principal, 'portal_quickinstaller')
    except:
        return
    if inst.isProductInstalled('hejasverige.content'):
        userid = event.principal.getId()
        logger.info('Creating content folders for %s' % str(userid))

        _getFolder(userid, 'my-family', 'Folder')
        _getFolder(userid, 'my-clubs', 'hejasverige.relationfolder')


def _getFolder(userid, id, type_name):
    context = getSite()
    typestool = getToolByName(context, 'portal_types')
    mship = getToolByName(context, 'portal_membership')
    current_auth = mship.getAuthenticatedMember()
    homefolder = mship.getHomeFolder(userid)
    logger.info('Found home folder %s' % str(homefolder))
    if homefolder is None:
        try:
            mship.createMemberarea(userid)
        except Exception as e:
            logger.info('Could not create member area: %s' % str(e))

        homefolder = mship.getHomeFolder(userid)
        logger.info('Homefolder = %s' % str(homefolder))

    if not id in homefolder.objectIds():
        typestool.constructContent(type_name=type_name,
                                   container=homefolder, id=id)
        folder = homefolder[id]
        folder.reindexObject()
        newSecurityManager(context.REQUEST, current_auth)
    return homefolder[id]      