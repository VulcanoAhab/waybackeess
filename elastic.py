from datetime import datetime
from elasticsearch import Elasticsearch


_ELASTIC = Elasticsearch()


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
        doc=self._response.data
        index=self._response._index
        timestamp=self._response._timestamp
        datis=datetime.strptime(timestamp, '%Y%m')
        doc.update({'timestamp':datis})
        _ELASTIC.index(index=index,
                        doc_type='backeess',
                        id=timestamp,
                        body=doc)
