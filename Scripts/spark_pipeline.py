from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.clustering import LDA
import sys
import os

# Import our HDFS Manager utility
sys.path.append(os.path.abspath('.'))
from hdfs_manager import HDFSManager

def initialize_spark(hdfs_host='192.168.56.101'):
    """Initialize Spark Session with HDFS support"""
    spark = SparkSession.builder \
        .appName("SocialMediaAnalysis_PFE") \
        .config("spark.hadoop.fs.defaultFS", f"hdfs://{hdfs_host}:8020") \
        .getOrCreate()
    return spark

def run_pipeline():
    hdfs_host = '192.168.56.101'
    spark = initialize_spark(hdfs_host)
    
    # 1. HDFS Upload (if not already there)
    hdfs = HDFSManager(host=hdfs_host)
    local_data_path = 'data/Raw/dataset.csv'
    hdfs_data_path = '/user/cloudera/data/raw/dataset.csv'
    
    if os.path.exists(local_data_path):
        hdfs.makedirs('/user/cloudera/data/raw')
        hdfs.upload_file(local_data_path, hdfs_data_path)
    
    # 2. Load Data from HDFS
    print("Loading data from HDFS...")
    df = spark.read.csv(
        f"hdfs://{hdfs_host}:8020{hdfs_data_path}", 
        header=True, 
        inferSchema=True,
        multiLine=True,
        escape='"'
    )
    
    # 3. Data Cleaning
    print("Cleaning data...")
    # Convert date to timestamp and extract day
    df = df.withColumn("timestamp", F.to_timestamp("date")) \
           .filter(F.col("timestamp").isNotNull()) \
           .withColumn("day", F.to_date("timestamp"))
    
    # Clean engagement metrics
    for col in ["likeCount", "replyCount", "retweetCount", "viewCount"]:
        df = df.withColumn(col, F.col(col).cast("float")).fillna(0, subset=[col])
        
    # 4. Topic Modeling (LDA)
    print("Running Topic Modeling...")
    # Preprocess text
    df_text = df.select("content").filter(F.col("content").isNotNull())
    
    tokenizer = Tokenizer(inputCol="content", outputCol="words")
    words_data = tokenizer.transform(df_text)
    
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    filtered_data = remover.transform(words_data)
    
    cv = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=1000, minDF=10)
    cv_model = cv.fit(filtered_data)
    vectorized_data = cv_model.transform(filtered_data)
    
    # Train LDA
    lda = LDA(k=5, maxIter=10) # 5 topics for now
    lda_model = lda.fit(vectorized_data)
    
    # Describe topics
    vocab = cv_model.vocabulary
    topics = lda_model.describeTopics(5)
    print("Topics identified:")
    topics.show()
    
    # 5. Export results for Power BI
    print("Exporting results for Power BI...")
    # Daily aggregation (Sentiment & Volume)
    # Note: Using simple sentiment logic for now as a placeholder
    daily_stats = df.groupBy("day").agg(
        F.count("*").alias("tweet_count"),
        F.sum("likeCount").alias("total_likes"),
        F.sum("retweetCount").alias("total_retweets")
    ).orderBy("day")
    
    daily_stats.toPandas().to_csv('data/Processed/daily_stats_spark.csv', index=False)
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
