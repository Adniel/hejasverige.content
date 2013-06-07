from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig

class SwedwiseEstimate(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import hejasverige.content
        xmlconfig.file('configure.zcml', hejasverige.content, context=configurationContext)
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'hejasverige.content:default')

HEJASVERIGE_CONTENT_FIXTURE = SwedwiseEstimate()
HEJASVERIGE_CONTENT_INTEGRATION_TESTING = IntegrationTesting(bases=(HEJASVERIGE_CONTENT_FIXTURE,), name="HejaSverigeContent:Integration")
HEJASVERIGE_CONTENT_ROBOT_TESTING = FunctionalTesting(bases=(AUTOLOGIN_LIBRARY_FIXTURE, HEJASVERIGE_CONTENT_FIXTURE, z2.ZSERVER), name="HejaSverigeContent:Robot")