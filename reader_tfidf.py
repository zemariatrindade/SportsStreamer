from pyspark.sql import SparkSession
import nltk
from nltk.corpus import stopwords
from pyspark.sql.functions import col, window, lower, regexp_replace, udf, explode, array, struct, lit, row_number, collect_list
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, ArrayType, DoubleType
from pyspark.ml.feature import Tokenizer, CountVectorizer, IDF
from pyspark.ml import Pipeline
from pyspark.sql import Window as W


# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

def read_and_process():
    # Start Spark session
    spark = SparkSession.builder \
        .appName("reddit_tfidf_reader") \
        .getOrCreate()

    # Set log level to ERROR to reduce the amount of log output
    spark.sparkContext.setLogLevel("ERROR")

    # Define the schema for the incoming JSON data with the right data types
    schema = StructType([
        StructField("comment", StringType(), True),
        StructField("prev_comment", StringType(), True),
        StructField("post", StringType(), True),
        StructField("author", StringType(), True),
        StructField("created_utc", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    # Read the JSON files as a stream
    json_df = spark.readStream \
        .schema(schema) \
        .format("json") \
        .option("path", "data/raw") \
        .option("maxFilesPerTrigger", 10) \
        .load()

    # Lowering case and removing special characters
    cleaned_df = json_df.withColumn("comment", lower(col("comment")))
    cleaned_df = cleaned_df.withColumn("comment", regexp_replace(col("comment"), "[^a-zA-Z\\s]", ""))

    # Broadcast stopwords
    stop_words = stopwords.words('english')
    broadcast_stopwords = spark.sparkContext.broadcast(stop_words)

    # Define UDF to remove stop words
    @udf(StringType())
    def remove_stopwords(text):
        list_of_words = [word for word in text.split() if word not in broadcast_stopwords.value]
        filtered_comment = " ".join(list_of_words)
        return filtered_comment

    # Apply the UDF to remove stop words
    cleaned_df = cleaned_df.withColumn("filtered_comment", remove_stopwords(col("comment")))

    tokenizer = Tokenizer(inputCol="text", outputCol="words")

    # Apply CountVectorizer to get term frequency
    cv = CountVectorizer(
        inputCol="words", outputCol="rawFeatures", vocabSize=1000, minDF=1.0
    )

    # Apply IDF to get TF-IDF
    idf = IDF(inputCol="rawFeatures", outputCol="features")

    # Define a pipeline
    pipeline = Pipeline(stages=[tokenizer, cv, idf])

    # Register UDF to convert sparse vector to dense vector
    def to_array(v):
        if v is None:
            return None
        return v.toArray().tolist()

    to_array_udf = udf(to_array, ArrayType(DoubleType()))
    spark.udf.register("to_array_udf", to_array_udf)

    # Apply windowing
    windowed_df = cleaned_df.groupBy(window(col("timestamp"), "60 seconds", "60 seconds")).agg(
        collect_list("filtered_comment").alias("texts")
    )

    def process_window(df, batch_id):
        for row in df.collect():
            window_start, window_end = row["window"]["start"], row["window"]["end"]
            texts = row["texts"]

            # Create a DataFrame for the texts in the window
            texts_df = spark.createDataFrame([(text,) for text in texts], ["text"])

            # Fit the pipeline to the data
            model = pipeline.fit(texts_df)

            # Transform the data
            tfidf_df = model.transform(texts_df)

            # Extract the vocabulary and TF-IDF features
            vocab = model.stages[1].vocabulary

            tfidf_df = tfidf_df.withColumn("tfidf_values", to_array_udf(col("features")))

            # Explode the features column to get individual words and their TF-IDF scores
            exploded_df = tfidf_df.select(
                explode(
                    array(
                        [
                            struct(
                                lit(vocab[i]).alias("word"),
                                col("tfidf_values")[i].alias("tfidf"),
                            )
                            for i in range(len(vocab))
                        ]
                    )
                ).alias("word_tfidf")
            )

            # Select word and tfidf score
            top_words_df = exploded_df.select("word_tfidf.word", "word_tfidf.tfidf")

            # Get top 10 words based on TF-IDF scores
            window_spec = W.orderBy(col("tfidf").desc())
            top_words_df = top_words_df.withColumn(
                "rank", row_number().over(window_spec)
            ).filter(col("rank") <= 10)

            # Add window information
            top_words_df = top_words_df.withColumn(
                "window_start", lit(window_start)
            ).withColumn("window_end", lit(window_end))

            top_words_df.show(truncate=False)

    query = windowed_df.writeStream \
        .outputMode("update") \
        .foreachBatch(process_window) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    read_and_process()


