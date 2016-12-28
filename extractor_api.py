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
        return etree.tostring(els[0])

    @classmethod
    def mine_elements(cls, xshot, target_path):
        '''
        '''
        els=xshot.xpath('{}'.format(target_path))
        if not els:return
        return [etree.tostring(el) for el in els]

    @classmethod
    def mine_links(cls, xshot):
        '''
        '''
        links=xshot.iterlinks()
        return [l[-2] for l in links]

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

        base={
            'page':snapshot,
            'retrieved_time':datetime.datetime.utcnow(),
            'head':self.mine_element(xshot,'.//head' ),
            'body':self.mine_element(xshot, './/body[@id="glb-doc"]'),
            'scripts':'\n\n'.join(self.mine_elements(xshot, './/script')),
            'links':self.mine_links(xshot)
        }

        for field,parser_dict in self._parsers.items():
            base[field]=parser_dict['fn'](base[parser_dict['section']])
        return base
