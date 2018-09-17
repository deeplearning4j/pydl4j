import jnius_config
import os
import warnings
import pydl4j

pydl4j.validate_datavec_jars()


from jnius import autoclass

SparkConf = autoclass('org.apache.spark.SparkConf')
SparkContext = autoclass('org.apache.spark.api.java.JavaSparkContext')
JavaRDD = autoclass('org.apache.spark.api.java.JavaRDD')
SparkTransformExecutor = autoclass('org.datavec.spark.transform.SparkTransformExecutor')
StringToWritablesFunction = autoclass('org.datavec.spark.transform.misc.StringToWritablesFunction')
WritablesToStringFunction = autoclass('org.datavec.spark.transform.misc.WritablesToStringFunction')


spark_conf = SparkConf()
spark_conf.setMaster('local[*]')
spark_conf.setAppName('test')
