import re
from functools import partial

from parser_api import Simple


######################################################Wayback simple parser

rex_analytics=re.compile(r'(?P<data>UA-[\w\d]+(?:-\d+)?)', re.I)
face_app=re.compile(r'"fb\:app\_id" content=(?P<data>"[^"])',re.I)
face_admin=re.compile(r'"fb\:admins" content=(?P<data>"[^"])', re.I)


def miner(target_string, fn):
    '''
    '''
    m=fn.search(target_string)
    if not m:return
    return m.group('data')


mine_analytics=partial(miner, fn=rex_analytics)
mine_app_id=partial(miner, fn=face_app)
mine_admin_id=partial(miner, fn=face_admin)


Ways=Simple()
Ways.set_parser('google_analytics', mine_analytics)
Ways.set_parser('facebook_app_id',mine_app_id)
Ways.set_parser('facebook_admin_id',mine_admin_id)
