
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder.appName("StreamingUsage").config("spark.sql.extensions","io.delta.sql.DeltaSparkSessionExtension").config("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate()

schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("device", StringType()),
    StructField("ts", StringType())
])

# For demo: read from socket text stream (nc -lk 9999) instead of Kafka
df_raw = spark.readStream.format("socket").option("host","localhost").option("port",9999).load()

json_df = df_raw.select(from_json(col("value"), schema).alias("e")).select("e.*").withColumn("ts", col("ts").cast(TimestampType()))

agg = json_df.groupBy(window(col("ts"), "1 minute"), col("event_type")).agg(count("*").alias("events"))

query = agg.writeStream.format("delta").outputMode("complete").option("checkpointLocation","/tmp/delta/check").start("/tmp/delta/usage_agg")

query.awaitTermination()
