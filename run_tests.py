# -*- coding: utf-8 -*-

import unittest
import sys
from tests import AnswersTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AnswersTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
