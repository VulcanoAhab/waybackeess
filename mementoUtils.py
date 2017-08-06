import re
import datetime

class Reader:
    """
    """
    _grabbers={
        "url":re.compile(r"<(?P<value>.*?)/?>"),
        "rel":re.compile(r"rel=\"(?P<value>.*?)\""),
        "date":re.compile(r"datetime=\"(?P<value>.*?)\""),
        "type":re.compile(r"type=\"(?P<value>.*?)\"")
    }

    @classmethod
    def grabValues(cls, targetValue):
        """
        """
        resDict={}
        for keyValue,rexFunc in cls._grabbers.items():
            res=rexFunc.search(targetValue)
            if not res:continue
            resValue=res.group("value")
            resDict[keyValue]=resValue
        return resDict

    def __init__(self, mementoData):
        """
        """
        self._raw=mementoData
        self._baseList=[]
        self._links=[]
        self._parse()

    def _parse(self):
        """
        """
        for line in self._raw.split("\n"):
            valuesDict=self.grabValues(line)
            if not valuesDict or not valuesDict.get("url"):continue
            self._baseList.append(valuesDict)
            if (not valuesDict["rel"]
               or "memento" not in valuesDict["rel"]):continue
            self._links.append(valuesDict)

    @property
    def rawResponse(self):
        """
        """
        return self._raw

    @property
    def fullResponse(self):
        """
        """
        return self._baseList

    @property
    def links(self):
        """
        """
        return self._links
