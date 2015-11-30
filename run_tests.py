# -*- coding: utf-8 -*-

import unittest
import sys
from tests import SimpleTest, DebugTest, AnswersTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(AnswersTest),
        unittest.makeSuite(DebugTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
