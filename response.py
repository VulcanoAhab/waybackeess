from datetime import datetime
import hashlib

from extractor import Ways

class Dateess:
    '''
    '''
    def __init__(self):
        '''
        '''
        self._d={'date_range':
                    {
                    'start':{'year':0, 'month':0},
                    'end':{'year':0, 'month':0}
                    }
                }
    @property
    def start_year(self):
        '''
        '''
        return self._d['date_range']['start']['year']

    @start_year.setter
    def start_year(self, year):
        '''
        '''
        self._d['date_range']['start']['year']=year

    @property
    def end_year(self):
        '''
        '''
        return self._d['date_range']['start']['year']

    @end_year.setter
    def end_year(self, year):
        '''
        '''
        self._d['date_range']['end']['year']=year

    @property
    def start_month(self):
        '''
        '''
        return self._d['date_range']['start']['month']

    @start_month.setter
    def start_month(self, month):
        '''
        '''
        self._d['date_range']['start']['month']=month

    @property
    def end_month(self):
        '''
        '''
        return self._d['date_range']['end']['month']

    @end_month.setter
    def end_month(self, month):
        '''
        '''
        self._d['date_range']['end']['month']=month

    def load(self, date_config):
        '''
        '''
        self._d=date_config



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

    @staticmethod
    def year_month(date_input):
        '''
        '''
        if isinstance(date_input, str):
            return datetime.strptime(date_input, '%Y%m')
        elif isinstance(date_input, datetime):
            return date_input.strftime('%Y%m')
        raise TypeError('Only string or datetime objects')

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
        'timestamp':Helpers.year_month(self.timestamp),
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
