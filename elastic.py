from datetime import datetime
from elasticsearch import Elasticsearch


_ELASTIC = Elasticsearch(host="127.0.0.1")

class Api:
    """
    """
    @staticmethod
    def save(index, doc_id, doc):
        """
        """
        _ELASTIC.index(index=index,
                        doc_type="backeess",
                        id=doc_id,
                        body=doc)
    @staticmethod
    def delete(index, doc_id):
        """
        """
        r=_ELASTIC.delete(index=index, doc_type="backeess", id=doc_id)
        print("[+] Deleted index:{} id:{}".format(index,doc_id))
        print(r)

    @staticmethod
    def delete_all(index):
        """
        """
        r=_ELASTIC.delete_by_query( index=index,
                                    doc_type="backeess",
                                    body={"query":{"match_all":{}}})
        deleted=r.get("deleted", "FAIL")
        print("[+] Delete {} from {}".format(deleted, index))


class Es:
    """
    """
    def __init__(self, snap_response):
        """
        """
        self._response=snap_response


    def save(self):
        """
        """
        doc=self._response.data
        index=self._response.report
        doc_id=self._response.id
        Api.save(index, doc_id, doc)
