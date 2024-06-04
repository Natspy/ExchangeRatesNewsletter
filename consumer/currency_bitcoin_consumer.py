from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

def run_consumer():
    # Kafka configuration
    KAFKA_BROKER = 'localhost:29092'
    CURRENCY_TOPIC = 'currency-rates'
    BITCOIN_TOPIC = 'bitcoin-rates'

    # Create Spark session
    spark = SparkSession.builder.appName("KafkaCurrencyBitcoinConsumer").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # Data schemas for JSON
    currency_schema = StructType([
        StructField("timestamp", LongType(), True),
        StructField("currency", StringType(), True),
        StructField("code", StringType(), True),
        StructField("rate", DoubleType(), True)
    ])

    bitcoin_schema = StructType([
        StructField("timestamp", LongType(), True),
        StructField("currency", StringType(), True),
        StructField("rate", DoubleType(), True)
    ])

    # Read data from Kafka
    currency_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", CURRENCY_TOPIC) \
        .load()

    bitcoin_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", BITCOIN_TOPIC) \
        .load()

    # Process JSON data
    currency_json_df = currency_df.selectExpr("CAST(value AS STRING) as json_value")
    currency_data_df = currency_json_df.select(from_json(col("json_value"), currency_schema).alias("data")).select("data.*")

    bitcoin_json_df = bitcoin_df.selectExpr("CAST(value AS STRING) as json_value")
    bitcoin_data_df = bitcoin_json_df.select(from_json(col("json_value"), bitcoin_schema).alias("data")).select("data.*")

    # Display data on console
    currency_query = currency_data_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    bitcoin_query = bitcoin_data_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    currency_query.awaitTermination()
    bitcoin_query.awaitTermination()
