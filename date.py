'''
Ugly - will be improved soon
'''

from datetime import datetime,timedelta

def archive_timestamp(timestamp):
    '''
    '''
    _d=datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    return _d.strftime('%Y%m%d')


def way_date(date_input):
    '''
    '''
    if isinstance(date_input, str):
        return datetime.strptime(date_input, '%Y%m%d')
    elif isinstance(date_input, datetime):
        return date_input.strftime('%Y%m%d')
    raise TypeError('Only string or datetime objects')

class Dateess:
    '''
    '''
    def __init__(self, full_year):
        '''
        '''
        self._d={'date_range':{
                'start':{'year':0, 'month':0, 'day':0},
                'end':{'year':0, 'month':0, 'day':0}}}
        self.full_year=full_year
        self._utc=datetime.utcnow()

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
        return self._d['date_range']['end']['year']

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

    @property
    def start_day(self):
        '''
        '''
        return self._d['date_range']['start']['day']

    @start_month.setter
    def start_day(self, day):
        '''
        '''
        self._d['date_range']['start']['day']=day

    @property
    def end_day(self):
        '''
        '''
        return self._d['date_range']['end']['day']

    @end_month.setter
    def end_day(self, day):
        '''
        '''
        self._d['date_range']['end']['day']=day

    @property
    def start_date(self):
        '''
        '''
        if not self.start_month:
            self.start_month=1
        if not self.start_day:
            self.start_day=1
        return datetime(year=self.start_year,
                        month=self.start_month,
                        day=self.start_day)
    @property
    def end_date(self):
        '''
        '''
        if not self.end_month:
            self.end_month=12
        if not self.end_day:
            self.end_day=31
        return datetime(year=self.end_year,
                        month=self.end_month,
                        day=self.end_day)

    @property
    def date_range(self):
        '''
        '''
        def sumday(date, days_size):
            '''
            '''
            new_date=date+timedelta(days=days_size)
            return way_date(new_date)
        ds=self.start_date
        de=self.end_date
        delta=de-ds
        return [sumday(ds,dn) for dn in range(delta.days+1)]

    @property
    def archive_timestamp(self):
        '''
        '''
        if not self._archive_stamp:
            raise TypeError('[-] Archive timestamp no set')
        return self._archive_stamp.strftime('%Y%m%d')

    @archive_timestamp.setter
    def archive_timestamp(self, archive_stamp):
        '''
        '''
        self._archive_stamp=datetime.strptime(archive_stamp, '%Y%m%d%H%M%S')

    def intime(self, archive_stamp):
        '''
        '''
        self.archive_timestamp=archive_stamp
        arquive_stamp=self._archive_stamp
        return (arquive_stamp >= self.start_date
                and arquive_stamp <= self.end_date)


    @staticmethod
    def load(site_config):
        '''
        '''
        if not 'date_range' in site_config:
            raise TypeError('[-] date_range is required')
        try:
            full_year=site_config['date_range'].pop('full_year')
            startis=site_config['date_range']['start']
            endis=site_config['date_range']['end']
        except KeyError as e:
            raise Exception('[-] Missing {} key'.format(e))
        if not 'year' in startis or not 'year' in endis:
            raise Exception('[-] Setting year range is required')
        dss=Dateess(full_year)
        dss.start_year=startis['year']
        dss.end_year=endis['year']
        if startis.get('month'):
            dss.start_month=startis['month']
            dss.end_month=endis['month']
        if startis.get('day'):
            dss.start_day=startis['day']
            dss.end_day=endis['day']
        return dss
