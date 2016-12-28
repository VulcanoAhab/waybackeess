from datetime import datetime
import hashlib

from extractor import Ways


class Helpers:
    '''
    '''
    @staticmethod
    def make_id(website, timestamp):
        '''
        '''
        m=hashlib.md5()
        m.update(''.join([website, timestamp]).encode())
        return m.hexdigest()

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
        self.timestamp=snap_dict['timestamp']
        self._data=self.parser.parse(self._raw['page'])
        self._data.update({
        'website':snap_dict['website'],
        'timestamp':datetime.strptime(self.timestamp, '%Y%m'),
        })
        self.id=Helpers.make_id(snap_dict['website'],self.timestamp)
        self.report=snap_dict['report']

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
