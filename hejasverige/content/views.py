from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot


class ReindexBrain(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('reindexbrain')

    def render(self):

        uid = self.request.form.get('uid') or None

        catalog = getToolByName(self.context, 'portal_catalog')

        query_dict = {}
        result = []
        result.append("<html><body><h1>Reindex object ")

        if uid:
            query_dict['UID'] = uid
            result.append("with UID " + query_dict['UID'] + "</h1>")

        brains = catalog(query_dict)
        #import pdb; pdb.set_trace()
        for brain in brains:
            try:
                res = brain.getObject().reindexObject()
                result.append(str(brain) + " reindexed")
            except Exception, ex:
                result.append("Exception " + str(ex) + " occured when reindexing " + str(brain))

        result.append('</body></html>')
        return "".join(result)
