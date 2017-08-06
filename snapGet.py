import requests
import datetime

from mementoUtils import Reader

class Availables(requests.Session):
    """
    """

    _base_map="http://web.archive.org/web/timemap/link/"

    def __init__(self, website):
        """
        """
        super().__init__()
        self.website=website
        self.headers={
            "User-Agent":"waybackess",
            "Accept":"text/html,application/xhtml+xml,"\
                     "application/xml;q=0.9,*/*;q=0.8",
            "Connection":"keep-alive",
        }
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
            self._resp["response"]["snaps"]=memsObject.links
        except Exception as e:
            print("[-] {}. Fail to fetch: {}".format(e, self.query))
            self._resp["response"]["error"]["message"]=respText
        self._resp["response"]["queryTime"]=datetime.datetime.utcnow()


    @property
    def response(self):
        """
        """
        return self._resp["response"]
