import datetime
import re
from lxml import html, etree



class Simple:
    '''
    '''
    _find_domain=re.compile(r'https?\:\/\/(?P<value>[^\/]+)')

    @classmethod
    def mine_element(cls, xshot, target_path):
        '''
        '''
        els=xshot.xpath('{}'.format(target_path))
        if not els:return
        return etree.tostring(els[0]).decode()

    @classmethod
    def mine_elements(cls, xshot, target_path):
        '''
        '''
        els=xshot.xpath('{}'.format(target_path))
        if not els:return []
        return [etree.tostring(el).decode() for el in els]

    @classmethod
    def mine_links(cls, xshot):
        '''
        '''
        def extract(ustring):
            '''
            '''
            domain=cls._find_domain.search(ustring)
            if not domain:return
            return domain.group('value')
        links=xshot.iterlinks()
        return [extract(l[-2])
                for l in links if 'http://' in l[-2]]

    @classmethod
    def mine_words(cls, xshot):
        '''
        '''
        els=xshot.xpath('.//*')
        return [e.text.strip()
                for e in els
                if ((e.text and len(e.text) > 7 and '\n' not in e.text)
                    and (e.tag and e.tag not in ['script','link']))]

    def __init__(self):
        '''
        '''
        self._extractors={}

    def set_extractor(self, field_name, extractorFn, section):
        '''
        '''
        self._extractors[field_name]={'fn':extractorFn,'section':section}

    @property
    def fields(self):
        '''
        '''
        return list(self._extractors.keys())

    def parse(self, snapshot):
        '''
        '''
        try:
            xshot=html.fromstring(snapshot)
            #basics
            base={
                'page':snapshot,
                'retrieved_time':datetime.datetime.utcnow(),
                'head':self.mine_element(xshot,'.//head' ),
                'body':self.mine_element(xshot, './/body[@id="glb-doc"]'),
                'scripts':'\n\n'.join(self.mine_elements(xshot, './/script')),
                'links':self.mine_links(xshot),
                'words':self.mine_words(xshot),
            }
        except:
            base={
                'page':snapshot,
                'retrieved_time':datetime.datetime.utcnow(),
                'head':'',
                'scripts':'',
                'links':[],
                'words':[]
                    }
        #add from extractor file
        for field,extractor_dict in self._extractors.items():
            base[field]=extractor_dict['fn'](base[extractor_dict['section']])
        return base

Ways=Simple()
