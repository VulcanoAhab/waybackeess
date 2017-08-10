
import re
import string
import datetime
import tldextract
from lxml import html


from operator import add
from pyspark.sql import Row
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, TimestampTime

# == udf[s]



# == process class
class Basic:
    """
    Need to implement transformations
    on scala udf to be called from python
    """
    _appName="wayBackeess"

    _spark=SparkSession.builder\
        .appName(_appName)\
        .getOrCreate()

    _wayLink=re.compile("(?:http://web.archive.org)?/web/\d+(?:im_)?/", re.I)

    _frameRow=Row(
        "raw",
        "urls",
        "words",
        "title",
        "website"
        "created_at",
        "captured_at"
    )

    _urlsRow=Row("url","domain")

    @classmethod
    def _getDomain(cls, urlIn):
        """
        """
        _exResult=cls._tdlex(urlIn)
        return _exResult.registered_domain

    @classmethod
    def toUrlObj(cls, urlIn):
        """
        """
        urlClean=cls._wayLink.sub("",urlIn)
        domain=cls._getDomain(urlClean)
        return self._urlsRow(url=urlClean, domain=domain)

    def __init__(self, pageIn, website, created_at):
        """
        """

        self._raw=pageIn
        self._website=webiste
        self._created=created_at

        self._rdd=self._spark.sparkContext.parallelize([pageIn])
        self._rdd.cache()
        self._df=None

    def findUrls(self, textIn):
        """
        """
        _xis=html.fromstring(textIn)

        _elsTarget={
            "href":"//@href",
            "src":"//@src",
            "data-src":"//@data-src"
        }
        _filterNot={
            lambda x:not x.startswith("/static/"),
        }

        #build lists
        _urls={}
        for attr,xpas in _elsTarget.items():
                #mine and filter urls
                ustemp=_xis.xpath(xpas)
                for condition in _filterNot:
                    ustemp=filter(condition, ustemp)
                #process urls
                for utemp in ustemp:
                    utemp=self.cleanUrl(utemp)
                    if attr not in _urls:_urls.update({attr:[]})
                    _urls[attr].append({
                        "url":utemp,
                        "domain":self._getDomain(utemp),
                        })
        return _urls

    def processWords(self):
        """
        """
        _words=self._rdd.flatMap(lambda x: x.split(" "))\
                                .map(lambda x: (x,1))\
                                .reduceByKey(add)
        self._wordsCount=_words.collect()
        print(self._wordsCount)

    def processUrls(self):
        """
        """
        _urls=self._rdd.flatMap(lambda x:self.findUrls(x))\
                                    .map(lambda x:self.toUrlObj(x))
        self._urls=_urls.collect()
        print(self._urls)

    def close(self):
        """
        """
        self._spark.stop()
