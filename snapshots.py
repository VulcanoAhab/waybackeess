import requests
import datetime
import time
import re
import urllib.parse as uparse


class Snap:
    '''
    '''

    _base='http://archive.org/wayback/available?url='

    @classmethod
    def _mount_request(cls, website, timestamp):
        '''
        '''
        return {
            'url':cls._base_url+website+timestamp,
            'timestamp':timestamp,
            'website':website,
            'id':'___'.join(website.replace('.','_'),timestamp),
                }

    @classmethod
    def _mount_stamp(cls, year, month):
        '''
        '''
        return '&timestamp='+year+month.zfill(2)

    @classmethod
    def set_data_selector(cls, selector_fn):
        '''
        '''
        pass

    def __init__(self, website):
        '''
        '''
        self._months=[]
        self._years=[]
        self._days=[]

        self.website=website
        self._times=[]
        self._snaps_queries=[]
        self._snaps_available=[]

        self._mount_queries()

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
        self._days=days_list

    def _mount_queries(self):
        '''
        '''
        self._snaps_queries=[self._mount_request(self.website,self._mount_stamp(*t))
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
            snap=snap['archived_snapshots']
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
        for snap_url in self._snaps_available:
