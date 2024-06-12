from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import from_json, col, from_unixtime, regexp_extract, window, count


def activate_streaming():
    # Start Spark session
    spark = SparkSession.builder \
        .appName("reddit_consumer_raw") \
        .getOrCreate()

    # Set log level to ERROR to reduce the amount of log output
    spark.sparkContext.setLogLevel("ERROR")

    # Step 1: Read data from the socket in string format
    raw_spark_df = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9998) \
        .load()

    # Step 2: Define the schema for the incoming JSON data with the right data types
    schema = StructType([
        StructField("comment", StringType(), True),
        StructField("prev_comment", StringType(), True),
        StructField("post", StringType(), True),
        StructField("author", StringType(), True),
        StructField("created_utc", DoubleType(), True)
    ])

    # Step 3: Parse the JSON data
    json_df = raw_spark_df.select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Convert created_utc to timestamp type
    json_df = json_df.withColumn("timestamp", from_unixtime(col("created_utc")))

    # Define the output path
    output_path = "data/raw"


    # 1st TODO: Write the parsed raw data to JSON files locally
    json_query = json_df.writeStream \
        .outputMode("append") \
        .format("json") \
        .option("path", output_path) \
        .option("checkpointLocation", "checkpoints/raw") \
        .trigger(processingTime="5 seconds") \
        .start()

    json_query.awaitTermination()


if __name__ == "__main__":
    activate_streaming()
