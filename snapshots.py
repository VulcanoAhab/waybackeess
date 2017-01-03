import requests
import datetime
import time
import re
import urllib.parse as uparse

from date import Dateess, archive_timestamp
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
    def _mount_stamp(cls, year, month, day):
        '''
        '''
        return '&timestamp='+year+month.zfill(2)+day.zfill(2)



    def __init__(self, website, report_name, dateess_obj):
        '''
        '''

        self.website=website
        self._times=[]
        self._snaps_queries=[]
        self._snaps_available=[]
        self.report=report_name
        self.dss=dateess_obj


    def _dates_list(self):
        '''
        '''
        self._times=[ (str(year),str(month),str(day))
                for year in self.dss.year_range
                for month in self.dss.month_range
                for day in self.dss.day_range]

    def mount_queries(self):
        '''
        '''
        self._dates_list()
        self._snaps_queries=[
            Snap._mount_request(self.website, Snap._mount_stamp(*t))
            for t in self._times]
        qty=len(self._snaps_queries)
        msg='[+] Queries {}. Target: {}'.format(qty, self.website)
        print(msg)

    @property
    def snaps_queries(self):
        '''
        '''
        return self._snaps_queries

    def map_availables(self):
        '''
        '''
        count_mapped=0
        unique_urls=set()
        for n,request_dict in enumerate(self._snaps_queries):
            url=request_dict['url']
            r=requests.get(url)
            r.raise_for_status()
            archive=r.json()
            snap=archive['archived_snapshots']
            size='[+] Requested: * {} *'.format(n)
            lsize=len(size)
            backis=lsize*'\r'
            print(backis+size, end='')
            if not snap:continue
            snap_url=snap['closest']['url']
            if snap_url in unique_urls:continue
            snap_stamp=snap['closest']['timestamp']
            snap_dict={
                'url':snap_url,
                'requested_timestamp':request_dict['timestamp'],
                'timestamp':archive_timestamp(snap_stamp),
                'website':request_dict['website'],
            }
            self._snaps_available.append(snap_dict)
            count_mapped+=1
            if count_mapped % 10 == 0:
                print(' Mapped {} snapshots'.format(count_mapped))
            unique_urls.add(snap_url)
            time.sleep(0.001)
        print('[+] Done mapping {} snapshots'.format(count_mapped))


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
