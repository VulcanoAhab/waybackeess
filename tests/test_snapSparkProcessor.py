import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))


import unittest
import snapSparkProcessor
from sparkUtils import SparkDo
# from snapSparkProcessor import buildDataFrame

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
        SparkDo.setAppName("waybackeess")
        self._sc=SparkDo.devTestContext()

    def tearDown(self):
        """
        just in case and to avoid warnings
        """
        self._fd.close()

    def test_processors(self):
        """
        """
        snapSparkProcessor.buildDataFrame(self.rawSnap, sparkContext=self._sc)

# == command line
if __name__ == "__main__":
    unittest.main()
