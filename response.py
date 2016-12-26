from parser import Ways

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
        self._id=snap_dict['timestamp']
        self._index=snap_dict['website']
        self._data=self.parser.parse(self._raw['page'])

    def get_parsed(self):
        '''
        '''
        return {k:v for k,v in self._data.items() if k != 'page'}

    def get_raw_page(self):
        '''
        '''
        return self._data['page']



WayDefault.set_parser(Ways)
