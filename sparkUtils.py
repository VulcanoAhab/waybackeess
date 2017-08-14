import logging
from pyspark import SparkContext, SparkConf

class SparkDo:
    """
    """
    _appName=None

    @classmethod
    def setAppName(cls, name):
        """
        """
        cls._appName=name

    @classmethod
    def devContext(cls):
        """
        """

        _conf = SparkConf()
        _conf.set("spark.executor.memory", "1g")
        _conf.set("spark.app.name", cls._appName)
        _sc = SparkContext(conf=_conf, pyFiles=[
                                            "snapSparkProcessor.py",
                                            "sparkUtils.py"
                                                ])
        #quiet context
        logger = logging.getLogger('py4j')
        logger.setLevel(logging.WARN)

        return _sc

    @classmethod
    def devTestContext(cls):
        """
        """
        _conf = SparkConf()
        _conf.set("spark.executor.memory", "1g")
        _conf.set("spark.app.name", cls._appName)
        _sc = SparkContext(conf=_conf, pyFiles=[
                                        "../snapSparkProcessor.py",
                                        "../sparkUtils.py",
                                        ])
        #quiet context
        logger = logging.getLogger('py4j')
        logger.setLevel(logging.WARN)

        return _sc
