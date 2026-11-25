import unittest

class DeploymentAcceptance(unittest.TestCase):
    @unittest.skip("Required controlled deployment is unavailable in this workspace; no live export evidence captured")
    def test_download_contains_real_query_result(self):
        raise AssertionError("Run against the controlled deployment with real query/download evidence")
