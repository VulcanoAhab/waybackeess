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
        self._modeled=cls.parse.parse(self._raw['page'])



WayDefault.set_parser(Ways)
