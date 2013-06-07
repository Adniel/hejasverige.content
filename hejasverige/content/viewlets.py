from five import grok
from plone.app.layout.viewlets.interfaces import IPortalTop
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from hejasverige.content.interfaces import IMyPages

grok.viewletmanager(IPortalTop)
grok.context(Interface)
grok.templatedir("templates")


class MenuBar(grok.Viewlet):
    """ Create a viewlet for transactions

    """
    grok.name('menubar')

    def update(self):
        self.mymenu_actions = []
        mship = getToolByName(self.context, 'portal_membership')
        if mship.isAnonymousUser():
            return

        if not IMyPages.providedBy(self.__parent__):
            return

        super(MenuBar, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        #tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')

        try: # Plone 4+
            self.mymenu_actions = context_state.actions(category="hejasverige.mymenu")
        except TypeError: # Plone 3
            self.mymenu_actions = context_state.actions().get('hejasverige.mymenu', ())

        #for action in self.mymenu_actions:
        #    if action['id'] == 'receivedmessages':
        #        catalog = getToolByName(self.context, 'portal_catalog')
        #        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        #        member = portal_state.member()
        #        action['unread'] = len(catalog(object_provides=IReceivedMessage.__identifier__, 
        #                                       path={'query': '%s/received' % '/'.join(mship.getHomeFolder(member.getId()).getPhysicalPath())},
        #                                       read=False))

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        #import pdb; pdb.set_trace()