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
    _available_urls=re.compile(r'<([^>]+)')
    _snap_stamp=re.compile(r'(?P<value>\d{14})')
    _base_closest='http://archive.org/wayback/available?url='
    _base_map='http://web.archive.org/web/timemap/link/'

    def __init__(self, website, report_name, dateess_obj):
        '''
        '''
        self.website=website
        self._snaps_available=[]
        self.report=report_name
        self.dss=dateess_obj

    def map_availables(self):
        '''
        '''
        count_mapped=0
        print('[+] Start mapping snaps for {}'.format(self.website))
        _url=''.join([self._base_map,self.website])
        try:
            r=requests.get(_url)
            r.raise_for_status()
        except Exception as e:
            print('[-] {}. Fail to map: {}'.format(e, _url))
            return
        snap_urls=self._available_urls.findall(r.text)
        if not snap_urls:
            print('[+] No snapshot available')
            return
        for snap_url in snap_urls:
            stamp_search=self._snap_stamp.search(snap_url)
            if not stamp_search: continue
            snap_stamp=stamp_search.group('value')
            if not self.dss.intime(snap_stamp):continue
            snap_dict={
                'url':snap_url,
                'timestamp':self.dss.archive_timestamp,
                'website':self.website,
            }
            self._snaps_available.append(snap_dict)
            count_mapped+=1
            if count_mapped % 10 == 0:
                print(' Mapped {} snapshots'.format(count_mapped))
            time.sleep(0.001)
        print('[+] Done mapping {} snapshots'.format(count_mapped))


    def fetch_availables(self):
        '''
        '''
        for snap_dict in self._snaps_available:
            try:
                r=requests.get(snap_dict['url'])
                r.raise_for_status()
            except Exception as e:
                print('[-] {}. Fail to fetch: {}'.format(e, snap_dict['url']))
                continue
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
