import requests
import datetime
import time

from mementoUtils import Reader

# == Globals
_HEADERS={
    "User-Agent":"waybackess",
    "Accept":"text/html,application/xhtml+xml,"\
             "application/xml;q=0.9,*/*;q=0.8",
    "Connection":"keep-alive",
}

# == Map Snapshots
class Availables(requests.Session):
    """
    """

    _base_map="http://web.archive.org/web/timemap/link/"

    @staticmethod
    def _baseDate(dateIn):
        """
        """
        if not dateIn:return None
        try:
            datis=datetime.datetime.strptime(dateIn,"%Y-%M")
        except Exception as e:
            print("[-] Fail to transform date: {}".format(e))
            datis=None
        return datis

    @staticmethod
    def _startDate(dateIn):
        """
        """
        return Availables._baseDate(dateIn)

    @staticmethod
    def _endDate(dateIn):
        """
        """
        datis=Availables._baseDate(dateIn)
        if not datis:return None
        return datis-datetime.timedelta(days=1)


    def __init__(self, website, start=None, end=None):
        """
        start|end : format => Year-Month
        """
        super().__init__()
        self.website=website
        self.start=Availables._startDate(start)
        self.end=Availables._endDate(end)
        self.headers=_HEADERS
        self._resp={"response":{
                            "snaps":[],
                            "queryTime":None,
                            "status":None,
                            "error":{"message":None},
                            },
                    }
        self.query="".join([self._base_map,self.website])

    def __del__(self):
        """
        """
        self.close()

    def fetch(self):
        """
        """
        try:
            resp=self.get(self.query)
            self._resp["response"]["status"]=resp.status_code
            resp.raise_for_status()
            respText=resp.text
            memsObject=Reader(respText)
            for respLink in memsObject.links:
                #filter date range if set
                if self.start:
                    respDate=respLink["date"]
                    if respDate<self.start:continue
                if self.end:
                    respDate=respLink["date"]
                    if respDate>self.end:continue
                respLink["website"]=self.website
                self._resp["response"]["snaps"].append(respLink)
        except Exception as e:
            print("[-] {}. Fail to fetch: {}".format(e, self.query))
            self._resp["response"]["error"]["message"]=respText
        self._resp["response"]["queryTime"]=datetime.datetime.utcnow()

    @property
    def response(self):
        """
        """
        return self._resp["response"]

# == Fecth Snapshots
class FetchSnaps(requests.Session):
    """
    """

    def __init__(self, targets, limit=0):
        """
        targets : list | format => {
                            "url":..., - required
                            "date":.., - required
                            "website":..,
                        }
        """
        super().__init__()
        self._targets=targets
        self.headers=_HEADERS
        self.limit=limit
        self._response={
            "snapshots":[],
        }


    def __del__(self):
        """
        """
        self.close()

    def run(self):
        """
        """
        targets=self._targets
        if self.limit:
            targets=targets[:self.limit]
        for snapDict in targets:
            response=self.get(snapDict["url"])
            snapshot=response.text
            self._response["snapshots"].append({
                                    "snapshot":snapshot,
                                    "url":snapDict["url"],
                                    "status":response.status_code,
                                    "queryTime":datetime.datetime.utcnow(),
                                    "date":snapDict["date"],
                                    "website":snapDict.get("website"),
                                    })
            time.sleep(0.01)

    @property
    def response(self):
        """
        """
        return self._response["snapshots"]
