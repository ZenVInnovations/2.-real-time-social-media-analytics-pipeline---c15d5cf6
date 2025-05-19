import os
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Set correct Python environment for Spark
os.environ["PYSPARK_PYTHON"] = "python"

print("✅ Starting Spark session...")
spark = SparkSession.builder \
    .appName("SentimentModelLocal") \
    .master("local[*]") \
    .config("spark.ui.enabled", "false") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .getOrCreate()

print("✅ Spark session started.")

# Load model
print("📦 Loading trained model...")
model = PipelineModel.load("sentiment_model")

# Load test CSV
print("📥 Loading twitter_training.csv...")
df = spark.read.csv("twitter_training.csv", header=False, inferSchema=True)
df = df.toDF("ID", "Entity", "Sentiment", "Tweet content")
df = df.filter(df["Tweet content"].isNotNull())

# Run prediction
print("🔮 Predicting sentiments...")
predictions = model.transform(df)

# Show results
predictions.select("Tweet content", "Sentiment", "prediction").show(10)

print("✅ Prediction complete.")