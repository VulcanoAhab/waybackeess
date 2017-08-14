
import re
import os
import string
import datetime
import tldextract
import logging
from lxml import html
from operator import add

from sparkUtils import SparkDo

from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql import Row, SparkSession
from pyspark import SparkContext, SparkConf

# == helpers functions

# - presets
_tdlex=tldextract.TLDExtract()
_wayLink=re.compile("(?:http://web.archive.org)?/web/\d+(?:im_)?/", re.I)
_grabUrl=re.compile(r"http://[\w\d\/\-\.\:]+") #need to be improve
_cleanText=re.compile(r"["+string.punctuation+"\n]+")

_frameRow=Row(
    "raw",
    "urls",
    "words",
    "title",
    "website"
    "created_at",
    "captured_at"
)



# -- base functions

def _toUrlObj(urlIn):
    """
    """
    cleanUrl=_wayLink.sub("", urlIn)
    _exResult=_tdlex(urlIn)
    domain=_exResult.registered_domain
    return {"url":cleanUrl,
            "domain":domain}



def toSnapRow(textIn, website=None, created_at=None):
    """
    """
    noScript="//*[text() and not(@type='text/javascript') "\
             "and not(contains(text(),'<!--'))]/text()"
    _xis=html.fromstring(textIn)
    rawTexts=_xis.xpath(noScript)
    #mine  text and words
    minLen=4
    texts=[]
    for rawText in rawTexts:
        cleanText=_cleanText.sub("",rawText).replace("\\","")
        if not cleanText or len(cleanText)<minLen:continue
        texts.append(cleanText)
    _text=" ".join(texts)
    #mine url
    rawUrls=_grabUrl.findall(textIn)
    filteredUrls=list(filter(lambda x:not x.startswith("/static/"),rawUrls))
    urlObjs=list(map(_toUrlObj,filteredUrls))
    onlyRow=Row(urlsMap=urlObjs,
                text=_text,
                raw=textIn,
                createad_at=created_at,
                website=website)
    return onlyRow

def saveRddEs(SnapRdd):
    """
    """
    SnapRdd.saveAsNewAPIHadoopFile(
    path='-',
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf={ "es.resource" : "waybackeess/testrun" })

## -- call functions

def transformAndSaveSnaps(websiteSnaps, sparkContext=None):
    """
    """
    #build context and transform data
    SparkDo.setAppName="waybackeess"
    _sc=sparkContext if sparkContext else SparkDo.devContext()
    _rdd=_sc.parallelize([websiteSnaps])
    _snapsRdd=_rdd.flatMap(lambda x: toSnapRow(x))
    #save
    #saveRddEs(_snapsRdd)
    _snapsRdd.saveAsNewAPIHadoopFile(
    path='-',
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf={ "es.resource" : "waybackeess/testrun" })
