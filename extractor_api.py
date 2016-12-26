import datetime

class Simple:
    '''
    '''

    def __init__(self):
        '''
        '''
        self._parsers={}

    def set_parser(self, field_name, parserFn):
        '''
        '''
        self._parsers[field_name]=parserFn

    @property
    def fields(self):
        '''
        '''
        return list(self._parsers.keys())

    def parse(self, mined_text):
        '''
        '''
        base={
            'page':mined_text,
            'retrieved_time':datetime.datetime.utcnow(),
        }
        for field,parser_fn in self._parsers.items():
            base[field]=parser_fn(mined_text)
        return base
