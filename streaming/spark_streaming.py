"""Spark Structured Streaming integration template.
Run in a Spark environment with the Kafka connector package.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

spark=SparkSession.builder.appName('RetailSalesStreaming').getOrCreate()
schema=StructType([StructField('event_id',StringType()),StructField('event_ts',StringType()),StructField('store_id',IntegerType()),StructField('region',StringType()),StructField('product_id',IntegerType()),StructField('customer_id',IntegerType()),StructField('quantity',IntegerType()),StructField('unit_price',DoubleType()),StructField('payment_method',StringType())])
raw=spark.readStream.format('kafka').option('kafka.bootstrap.servers','localhost:9092').option('subscribePattern','sales-.*').option('startingOffsets','earliest').load()
parsed=raw.select(from_json(col('value').cast('string'),schema).alias('e')).select('e.*')
query=parsed.writeStream.format('console').option('checkpointLocation','./checkpoints/sales').outputMode('append').start()
query.awaitTermination()
