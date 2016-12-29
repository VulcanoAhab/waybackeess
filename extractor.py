import re
from functools import partial

from extractor_api import Ways

# ##################### set a new extractor:
#     Way.set_extractor(field_name, extractor_fucntion, page_section)
#     page_section options are:
#         a. page [full snapshot]
#         b. head
#         c. scripts

rex_analytics=re.compile(r'(?P<data>UA-[\w\d]+(?:-\d+)?)', re.I)
face_app=re.compile(r'"fb\:app\_id" content="(?P<data>[^"]+)',re.I)
face_admin=re.compile(r'"fb\:admins" content="(?P<data>[^"]+)', re.I)


def miner(target_string, fn):
    '''
    '''
    if not target_string:return
    m=fn.search(target_string)
    if not m:return
    return m.group('data')


mine_analytics=partial(miner, fn=rex_analytics)
mine_app_id=partial(miner, fn=face_app)
mine_admin_id=partial(miner, fn=face_admin)


def mine_text(target_page):
    '''
    '''
    xpathis=html.fromstring()



Ways.set_extractor('google_analytics', mine_analytics, 'scripts')
Ways.set_extractor('facebook_app_id',mine_app_id, 'head')
Ways.set_extractor('facebook_admin_id',mine_admin_id, 'head')
