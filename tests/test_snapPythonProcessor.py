import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from snapPythonProcessor import Basic
import unittest

class TestBasic(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        #load file
        self._fd=open("testSnapHtml.txt")
        self.rawSnap=self._fd.read()
        self._fd.close
        self._basic=Basic(self.rawSnap)
        #full count
        self.refsCount=self.rawSnap.count("href=")
        self.srcCount=self.rawSnap.count("src=")
        self.dataSrcCount=self.rawSnap.count("data-src=")
        #filtered -- wayback urls
        self.WayRefsCount=self.rawSnap.count("href=\"/static/")
        self.WaySrcCount=self.rawSnap.count("src=\"/static/")
        self._counts={
            "href":self.refsCount-self.WayRefsCount,
            "src":self.srcCount-self.WaySrcCount
        }

    def tearDown(self):
        """
        just in case and to avoid warnings
        """
        self._fd.close()

    def testProcessUrls(self):
        """
        """
        shouldKeys={"href", "src"} #no test for data-src
        uDictKeys={"url", "domain"}
        testUrls=self._basic.urls
        for sk in shouldKeys:
            self.assertIn(sk, testUrls)
            self.assertEqual(self._counts[sk], len(testUrls[sk]),
                             "[-] Fail Count: {}".format(sk))
            for uk in uDictKeys:
                self.assertIn(uk, testUrls[sk][0])

    def testProcessTitle(self):
        """
        """
        self.assertEqual("Universo Online", self._basic.title)

    def testProcessText(self):
        """
        """
        print(self._basic.text)

# == command line
if __name__ == "__main__":
    unittest.main()
