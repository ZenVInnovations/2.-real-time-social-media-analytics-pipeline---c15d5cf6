import os
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# Set Spark to use the current Python environment
os.environ["PYSPARK_PYTHON"] = "python"

# Step 1: Start Spark session (UI disabled)
print("✅ Building Spark Session...")
spark = SparkSession.builder \
    .appName("TwitterSentiment") \
    .master("local[*]") \
    .config("spark.ui.enabled", "false") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()
print("✅ Spark Session started.")

# Step 2: Confirm CSV file presence
print("📁 Checking current directory:")
for f in os.listdir('.'):
    print("   -", f)

# Step 3: Load CSV data
print("📥 Reading twitter_training.csv ...")
try:
    data = spark.read.csv("twitter_training.csv", header=True, inferSchema=True)
    print("✅ CSV loaded successfully.")
    data.printSchema()
except Exception as e:
    print("❌ Error loading CSV:", str(e))
    exit()

# Step 4: Preprocessing pipeline
print("🔄 Creating pipeline...")
try:
    tokenizer = Tokenizer(inputCol="Tweet content", outputCol="words")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    lr = LogisticRegression(labelCol="Sentiment", featuresCol="features")

    pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])
except Exception as e:
    print("❌ Error building pipeline:", str(e))
    exit()

# Step 5: Train model
print("🚀 Training model...")
try:
    model = pipeline.fit(data)
    print("✅ Model training complete.")
except Exception as e:
    print("❌ Error during training:", str(e))
    exit()

# Step 6: Save model
print("💾 Saving model to 'sentiment_model'...")
try:
    model.write().overwrite().save("sentiment_model")
    print("✅ Model saved successfully.")
except Exception as e:
    print("❌ Error saving model:", str(e))