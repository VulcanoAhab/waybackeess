from extractor import Ways

class WayDefault:
    '''
    '''

    @classmethod
    def set_parser(cls, ParserObj):
        '''
        '''
        cls.parser=ParserObj

    def __init__(self, snap_dict):
        '''
        '''
        self._raw=snap_dict
        self._timestamp=snap_dict['timestamp']
        self._index=snap_dict['website']
        self._data=self.parser.parse(self._raw['page'])

    @property
    def extracted(self):
        '''
        '''
        return {k:v for k,v in self._data.items() if k != 'page'}

    @property
    def snapshot(self):
        '''
        '''
        return self._data['page']

    @property
    def data(self):
        '''
        '''
        return self._data



WayDefault.set_parser(Ways)
