import re
import datetime

from functools import partial



class Basic:
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
            'text':mined_text,
            '_parsed_time':datetime.datetime.utcnow(),
        }
        for field,parser_fn in self.parsers.items():
            base[field]=parser(mined_text)
        return base




######################################################Wayback simple parser

rex_analytics=re.compile(r'UI-(?<data>[\w\d]+)(?:-\d+)?', re.I)
face_app=re.compile(r'"fb\:app\_id" content=(?<data>"[^"])',re.I)
face_admin=re.compile(r'"fb\:admins" content=(?<data>"[^"])', re.I)


def miner(target_string, fn):
    '''
    '''
    m=fn.search(target_string)
    if not m:return
    return m.group('data')


mine_analytics=partial(miner, fn=rex_analytics)
mine_app_id=partial(miner, fn=face_app)
mine_admin_id=partial(miner, fn=face_admin)


Ways=Basic()
Ways.set_parser('google_analytics', mine_analytics)
Ways.set_parser('facebook_app_id',mine_app_id)
Ways.set_parser('facebook_admin_id',mine_admin_id)
