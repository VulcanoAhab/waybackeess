
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
from pyspark.sql.types import StringType, TimestampType

# == udf[s]

_wayLink=re.compile("(?:http://web.archive.org)?/web/\d+(?:im_)?/", re.I)



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

    _sc=_spark.sparkContext
    _sc.setLogLevel("ERROR")


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

    def __init__(self, pageIn, website=None, created_at=None):
        """
        """

        self._raw=pageIn
        self._website=website
        self._created=created_at

        self._rdd=self._sc.parallelize([pageIn])
        self._rdd.cache()
        self._df=None

    def processWords(self):
        """
        """
        _words=self._rdd.flatMap(lambda x: re.split(r"\s+",x))\
                                .map(lambda x: (x,1))\
                                .reduceByKey(add)
        self._wordsCount=_words.collect()
        print(self._wordsCount)

    def processUrls(self):
        """
        """
        _urls=self._rdd.flatMap(lambda x:re.findall(r"http://[\w\d\/\-\.\:]+", x))\
                                    .map(lambda x:_wayLink.sub("",x))
        self._urls=_urls.collect()
        print(self._urls)

    def close(self):
        """
        """
        self._spark.stop()
