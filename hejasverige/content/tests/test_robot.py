import unittest

import robotsuite
from hejasverige.content.testing import HEJASVERIGE_CONTENT_ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('test_hello.robot'),
                layer=HEJASVERIGE_CONTENT_ROBOT_TESTING),
    ])
    return suite
