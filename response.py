from parser import Ways

class Response:
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



Response.set_parser(Ways)
