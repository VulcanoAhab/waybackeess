import datetime
from lxml import html, etree

class Simple:
    '''
    '''

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
        if not els:return
        return [etree.tostring(el).decode() for el in els]

    @classmethod
    def mine_links(cls, xshot):
        '''
        '''
        links=xshot.iterlinks()
        return [l[-2] for l in links]

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
        self._parsers={}

    def set_parser(self, field_name, parserFn, section):
        '''
        '''
        self._parsers[field_name]={'fn':parserFn,'section':section}

    @property
    def fields(self):
        '''
        '''
        return list(self._parsers.keys())

    def parse(self, snapshot):
        '''
        '''
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

        #extras
        for field,parser_dict in self._parsers.items():
            base[field]=parser_dict['fn'](base[parser_dict['section']])
        return base
