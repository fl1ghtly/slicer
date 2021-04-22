# Thanks to
# https://www.internalpointers.com/post/run-painless-test-suites-python-unittest
import unittest

import test.test_expand_search
import test.test_norm_coord

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test.test_expand_search))
suite.addTests(loader.loadTestsFromModule(test.test_norm_coord))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)