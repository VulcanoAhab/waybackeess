import re
import tldextract
import collections
from lxml import html


class Basic:
    """
    Basic Snapshot parse for HTML attribute
    extraction
    """
    _wayLink=re.compile("(?:http://web.archive.org)?/web/\d+(?:im_)?/", re.I)

    _tdlex=tldextract.TLDExtract()

    @classmethod
    def cleanUrl(cls, urlIn):
        """
        """
        urlIn=cls._wayLink.sub("",urlIn)
        return urlIn

    @classmethod
    def _getDomain(cls, urlIn):
        """
        """
        _exResult=cls._tdlex(urlIn)
        return _exResult.registered_domain

    def __init__(self, pageIn):
        """
        """
        self._raw=pageIn
        self._xis=html.fromstring(pageIn)


    def processUrls(self):
        """
        """
        urlsContainer=collections.defaultdict(list)
        _elsTarget={
            "href":"//@href",
            "src":"//@src",
            "data-src":"//@data-src"
        }
        _filterNot={
            lambda x:not x.startswith("/static/"),
        }
        #build lists
        for attr,xpas in _elsTarget.items():
                #mine and filter urls
                ustemp=self._xis.xpath(xpas)
                for condition in _filterNot:
                    ustemp=filter(condition, ustemp)
                #process urls
                for utemp in ustemp:
                    utemp=self.cleanUrl(utemp)
                    urlsContainer[attr].append({
                        "url":utemp,
                        "domain":self._getDomain(utemp),

                        })
        return urlsContainer
