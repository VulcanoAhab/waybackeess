
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
import re
from mementoUtils import Reader

class TestReader(unittest.TestCase):
    """
    """
    _rexMemento=re.compile(r'rel="memento"')
    _rexOriginal=re.compile(r'rel="original"')
    _rexTimeGate=re.compile(r'rel="timegate"')
    _rexSelfCount=re.compile(r'rel="self"')
    _rexFirstMemento=re.compile(r'rel="first memento"')

    def setUp(self):
        """
        """
        # == load test file
        self._fd=open("testMemento.txt", "r")
        self.MementoData=self._fd.read()
        self._fd.close

        # == build Reader instance
        self._rer=Reader(self.MementoData)

        # == build metadata
        self.countLines=len([r for r in self.MementoData.split("\n") if r])
        self.countFirstMemento=self._countFind(self._rexFirstMemento)
        self.countSelf=self._countFind(self._rexSelfCount)
        self.countTimeGate=self._countFind(self._rexTimeGate)
        self.countRelOriginal=self._countFind(self._rexOriginal)
        self.countRelMemento=self._countFind(self._rexMemento)
        self.mems=self.relCounter("memento")+self.relCounter("first memento")

    def tearDown(self):
        """
        """
        #ensure file closed :: avoid painful warning
        self._fd.close()

    # == helpers
    def _countFind(self, rexFunc):
        """
        """
        count=len([r for r in rexFunc.findall(self.MementoData) if r])
        return count

    def relCounter(self, relValue):
        """
        """
        count=len([r for r in self._rer.fullResponse
                   if r.get("rel")==relValue])
        return count

    def urlCounter(self):
        """
        """
        count=len([r for r in self._rer.fullResponse if r.get("url")])
        return count

    def dateTimeCounter(self):
        """
        """
        count=len([r for r in self._rer.fullResponse if r.get("date")])
        return count

    # == tests
    def test_fullReponse(self):
        """
        """

        # count
        self.assertEqual(len(self._rer.fullResponse), self.countLines)
        self.assertEqual(self.countFirstMemento, self.relCounter("first memento"))
        self.assertEqual(self.countSelf, self.relCounter("self"))
        self.assertEqual(self.countTimeGate, self.relCounter("timegate"))
        self.assertEqual(self.countRelOriginal, self.relCounter("original"))
        self.assertEqual(self.countRelMemento, self.relCounter("memento"))
        # structs
        self.assertEqual(self.countLines, self.urlCounter())
        self.assertEqual(self.dateTimeCounter(), self.mems)



    def test_links(self):
        """
        """
        self.assertEqual(self.mems, len(self._rer.links))



# == command line
if __name__ == "__main__":
    unittest.main()
