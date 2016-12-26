from datetime import datetime
from elasticsearch import Elasticsearch


#_ELASTIC = Elasticsearch()


class Es:
    '''
    '''
    def __init__(self, snap_response):
        '''
        '''
        self._response=snap_response


    def save(self):
        '''
        '''
        body=self._response.get_parsed()
        index=self._response._index
        _id=self._response._id
        #_ELASTIC.index(index=index,
        #                doc_type='backeess',
        #                id=_id,
        #                body=doc)
        print(self._response.get_parsed())
