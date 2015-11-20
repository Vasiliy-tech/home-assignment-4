# -*- coding: utf-8 -*-

import unittest
import sys
from tests import SimpleTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(SimpleTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
