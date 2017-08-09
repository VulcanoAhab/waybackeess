import re
import string
import tldextract
import collections
from lxml import html


class Basic:
    """
    Basic Snapshot parse for HTML attribute
    extraction
    """
    _wayLink=re.compile("(?:http://web.archive.org)?/web/\d+(?:im_)?/", re.I)
    _cleanText=re.compile(r"["+string.punctuation+"\n]+")

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
        self._urls=collections.defaultdict(list)
        self._text=None
        self._title=None

    def processUrls(self):
        """
        """

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
                    self._urls[attr].append({
                        "url":utemp,
                        "domain":self._getDomain(utemp),

                        })
    @property
    def urls(self, force=False):
        """
        """
        if len(self._urls) and not force:return self._urls
        self.processUrls()
        return self._urls

    def processText(self, minLen=4):
        """
        """
        texts=[]
        noScript="//*[text() and not(@type='text/javascript') "\
                 "and not(contains(text(),'<!--'))]/text()"
        for text in self._xis.xpath(noScript):
            text=self._cleanText.sub("",text).replace("\\","")
            if not text or len(text)<minLen:continue
            texts.append(text)
        self._text=" ".join(texts)

    @property
    def text(self, force=False):
        """
        """
        if self._text and not force:return self._text
        self.processText()
        return self._text

    def processTitle(self):
        """
        """
        title=self._xis.xpath("//title/text()")
        if not title:return
        self._title=title[0]

    @property
    def title(self, force=False):
        """
        """
        if self._title and not force: return self._title
        self.processTitle()
        return self._title
