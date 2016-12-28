import requests
import datetime
import time
import re
import urllib.parse as uparse

from response import WayDefault
from elastic import Es

class Snap:
    '''
    '''

    _base='http://archive.org/wayback/available?url='

    @classmethod
    def _mount_request(cls, website, timestamp):
        '''
        '''
        timees=timestamp.split('=')[-1]
        request_dict ={
            'url':cls._base+website+timestamp,
            'timestamp':timees,
            'website':website,
            'id':'___'.join([website.replace('.','_'),timees]),
                }
        return request_dict

    @classmethod
    def _mount_stamp(cls, year, month):
        '''
        '''
        return '&timestamp='+year+month.zfill(2)


    def __init__(self, website, report):
        '''
        '''
        self._months=[]
        self._years=[]
        self._days=[]

        self.website=website
        self._times=[]
        self._snaps_queries=[]
        self._snaps_available=[]
        self.full_year=False
        self.report=report

    def set_years(self, years_list):
        '''
        '''
        self._years=years_list

    def set_months(self, months_list):
        '''
        '''
        self._months=months_list


    def set_days(self, days_list):
        '''
        '''
        raise NotImplemented('[+] Days options not avaible yet')

    def _dates_list(self):
        '''
        '''
        now=datetime.datetime.utcnow()
        if not self._years:
            self._years=[now.year,]
        if not self._months:
            if self.full_year==False:
                self._months=[now.month,]
            else:
                self._months=list(range(1,13))
        self._times=[ (str(year),str(month))
                for year in self._years
                for month in self._months]

    def mount_queries(self):
        '''
        '''
        self._dates_list()
        self._snaps_queries=[
            Snap._mount_request(self.website, Snap._mount_stamp(*t))
            for t in self._times]

    @property
    def snaps_queries(self):
        '''
        '''
        return self._snaps_queries

    def map_availables(self):
        '''
        '''
        for request_dict in self._snaps_queries:
            url=request_dict['url']
            r=requests.get(url)
            r.raise_for_status()
            archive=r.json()
            snap=archive['archived_snapshots']
            if not snap:continue
            snap_url=snap['closest']['url']
            snap_dict={
                'url':snap_url,
                'timestamp':request_dict['timestamp'],
                'website':request_dict['website'],
            }
            self._snaps_available.append(snap_dict)
            time.sleep(0.001)


    def fetch_availables(self):
        '''
        '''
        for snap_dict in self._snaps_available:
            r=requests.get(snap_dict['url'])
            r.raise_for_status()
            page=r.text
            snap_dict['page']=page
            snap_dict['report']=self.report
            response=WayDefault(snap_dict)
            yield response


    def save_availables(self):
        '''
        '''
        count_save=0
        for response in self.fetch_availables():
            esobj=Es(response)
            esobj.save()
            count_save+=1
            if count_save % 10 == 0:
                print('[+] Saved {} snapshots'.format(count_save))
        print('[+] Done saving availables. Count: {}'.format(count_save))
