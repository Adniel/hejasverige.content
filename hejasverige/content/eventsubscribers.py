from five import grok
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from AccessControl.SecurityManagement import newSecurityManager


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
        print 'Creating content folders for %s' % str(userid)

        _getFolder(userid, 'my-family', 'Folder')
        _getFolder(userid, 'my-clubs', 'hejasverige.relationfolder')


def _getFolder(userid, id, type_name):
    context = getSite()
    typestool = getToolByName(context, 'portal_types')
    mship = getToolByName(context, 'portal_membership')
    current_auth = mship.getAuthenticatedMember()
    homefolder = mship.getHomeFolder(userid)
    print 'Found home folder %s' % str(homefolder)
    if homefolder is None:
        try:
            mship.createMemberarea(userid)
        except Exception as e:
            print 'Could not create member area'
            print str(e)

        homefolder = mship.getHomeFolder(userid)
        print 'Homefolder = %s' % str(homefolder)

    if not id in homefolder.objectIds():
        import pdb; pdb.set_trace()

        #user = self._getOwner(homefolder)
        #if not user:
        #    return None
        #newSecurityManager(context.REQUEST, user)
        typestool.constructContent(type_name=type_name,
                                   container=homefolder, id=id)
        folder = homefolder[id]
        folder.reindexObject()
        newSecurityManager(context.REQUEST, current_auth)
    return homefolder[id]      