from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, from_unixtime, to_timestamp, when, lit
from pyspark.sql.types import StructType, StructField, LongType, DoubleType
from pyspark.sql.types import IntegerType


# Kafka
KAFKA_BOOTSTRAP = "127.0.0.1:9092"

TOPIC = "sensor_data"

# PostgreSQL
PG_URL = "jdbc:postgresql://127.0.0.1:5432/ICS474_Pipeline"
PG_USER = "postgres"
PG_PASS = "NewStrongPass123"
PG_TABLE = "public.sensor_readings"   # explicit schema is safer

schema = StructType([
    StructField("timestamp", LongType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("pressure", DoubleType(), True),
    StructField("is_anomaly_source", IntegerType(), True),

])

spark = (
    SparkSession.builder
    .appName("KafkaToPostgres")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config("spark.hadoop.io.native.lib.available", "false")
    .config("spark.sql.adaptive.enabled", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)

json_df = raw_df.selectExpr("CAST(value AS STRING) AS json")

parsed = (
    json_df
    .select(from_json(col("json"), schema).alias("d"))
    .select("d.*")
)

# Drop bad parses
parsed = parsed.dropna(subset=["timestamp", "temperature", "humidity", "pressure"])

# IMPORTANT: if your producer timestamp is MILLISECONDS, replace col("timestamp") with (col("timestamp")/1000).cast("long")
df = (
    parsed
    .withColumn("ts", to_timestamp(from_unixtime(col("timestamp"))))
    .drop("timestamp")
)

# Add sensor_id to match your table schema (text column)
df = df.withColumn("sensor_id", lit("sensor_1"))

# Anomaly flag
df = df.withColumn(
    "anomaly_flag",
    when(
        (col("temperature") < 20) | (col("temperature") > 30) |
        (col("humidity") < 30) | (col("humidity") > 60) |
        (col("pressure") < 990) | (col("pressure") > 1010),
        1
    ).otherwise(0)
)

def write_to_postgres(batch_df, batch_id):
    try:
        count = batch_df.count()
        print(f"Batch {batch_id} -> rows={count}")
        if count == 0:
            return

        (batch_df.select("ts","sensor_id","temperature","humidity","pressure","anomaly_flag","is_anomaly_source")
         .write
         .format("jdbc")
         .option("url", PG_URL)
         .option("dbtable", PG_TABLE)
         .option("user", PG_USER)
         .option("password", PG_PASS)
         .option("driver", "org.postgresql.Driver")
         .mode("append")
         .save())

        print(f"Batch {batch_id} written to Postgres")
    except Exception as e:
        print(f"Batch {batch_id} FAILED writing to Postgres: {repr(e)}")



query = (
    df.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .option("checkpointLocation", "file:///C:/tmp/spark-checkpoints/kafka_to_pg_v2")
    .start()
)

query.awaitTermination()
