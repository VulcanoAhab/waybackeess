import re
from pyspark.sql.functions import udf
from pyspark.sql import SparkSession


class Basic:
    """
    """
    _appName="wayBackeess"
    _spark=SparkSession.builder\
        .appName(_appName)\
        .getOrCreate()

    def __init__(self, pageIn):
        """
        """
        self._raw=pageIn
        self._rdd=self._spark.sparkContext.parallelize([pageIn])

    @property
    def rdd(self):
        """
        """
        return self._rdd.collect()


    def close(self):
        """
        """
        self._spark.stop()
