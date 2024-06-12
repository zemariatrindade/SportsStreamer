from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import from_json, window, col, regexp_extract, count


def read_and_process():
    spark = SparkSession.builder \
        .appName("reddit_reference_reader") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Define the schema for the incoming JSON data
    schema = StructType([
        StructField("comment", StringType(), True),
        StructField("prev_comment", StringType(), True),
        StructField("post", StringType(), True),
        StructField("author", StringType(), True),
        StructField("created_utc", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    # Read the JSON files from the raw data directory
    json_df = spark.readStream \
        .schema(schema) \
        .format("json") \
        .option("path", "data/raw") \
        .load()
        #.option("maxFilesPerTrigger", 2) \



    # Extract references to users, posts, and external sites using regex
    user_ref_df = json_df.withColumn("reference", regexp_extract(col("comment"), r"/u/(\w+)", 0)).filter(
        col("reference") != "")
    post_ref_df = json_df.withColumn("reference", regexp_extract(col("comment"), r"/r/(\w+)", 0)).filter(
        col("reference") != "")
    url_ref_df = json_df.withColumn("reference", regexp_extract(col("comment"), r"(https://\S+)", 0)).filter(
        col("reference") != "")

    # Combine all references into a single DataFrame
    combined_df = user_ref_df.select("timestamp", "reference") \
        .union(post_ref_df.select("timestamp", "reference")) \
        .union(url_ref_df.select("timestamp", "reference"))

    """
    # Apply watermarking and windowing functions
    windowed_counts = combined_df \
        .withWatermark("timestamp", "2 minutes") \
        .groupBy(
        window(col("timestamp"), "60 seconds", "5 seconds"),
        col("reference")
    ) \
        .agg(
        count("reference").alias("count")
    ) \
        .select(
        col("reference"),
        col("count"))
    """
    # Apply watermarking and windowing functions
    windowed_counts = combined_df \
        .withWatermark("timestamp", "2 minutes") \
        .groupBy(
        window(col("timestamp"), "60 seconds", "5 seconds")
    ) \
        .agg(
        count("reference").alias("total_references")
    )


    # Output the windowed results to the console
    query = windowed_counts.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .option("checkpointLocation", "checkpoints/references") \
        .trigger(processingTime="5 seconds") \
        .start()

    query.awaitTermination()

    """"
    def print_batch(df, epoch_id):
        # Collect rows and print each row with custom formatting
        rows = df.collect()
        if rows:
            print(f"Batch: {epoch_id}")
            print("-------------------------------------------")
            for row in rows:
                print(f"{row['reference']} | {row['count']}")
            print("-------------------------------------------\n")

    windowed_counts_query = windowed_counts.writeStream \
        .outputMode("update") \
        .foreachBatch(print_batch) \
        .option("checkpointLocation", "checkpoints/references") \
        .trigger(processingTime="5 seconds") \
        .start()

    windowed_counts_query.awaitTermination()
    """

if __name__ == "__main__":
    read_and_process()
