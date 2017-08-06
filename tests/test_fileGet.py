import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from snapGet import Availables
import unittest
import requests

class TestAvailables(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.targetSite="uol.com.br"
        self._availables=Availables(self.targetSite)


    def testFetch(self):
        """
        """
        self._availables.fetch()
        self.assertEqual(200, self._availables.response["status"])

    def testResponse(self):
        """
        """
        self._availables.fetch()
        #structs
        for key in {"snaps", "status", "error", "queryTime"}:
            self.assertIn(key, self._availables.response,
                                "[-] MISSING {}".format(key))
        #required[s]
        self.assertTrue(self._availables.response["status"])
        self.assertTrue(self._availables.response["queryTime"])

        #response
        self.assertTrue(len(self._availables.response["snaps"])>0)


    def testHeader(self):
        """
        """
        headers=self._availables.headers
        userAg=headers["User-Agent"]
        query="https://httpbin.org/headers"
        r=self._availables.get(query)
        respUserAg=r.json()["headers"]["User-Agent"]
        self.assertEqual(userAg, respUserAg,
                         "[-] FAIL HEADERS: {}".format(respUserAg))



# == command line
if __name__ == "__main__":
    unittest.main()
