import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from snapSparkProcessor import Basic

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
        self._basic.close()

    def test_processors(self):
        """
        """
        self._basic.processUrls()
        self._basic.processWords()

# == command line
if __name__ == "__main__":
    unittest.main()
