from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from kafka import KafkaConsumer
from json import loads
import pickle
import re
import nltk
from pymongo import MongoClient

# Download stopwords and punkt
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Load model and vectorizer
with open("../logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# MongoDB setup
client = MongoClient("localhost", 27017)
db = client["bigdata_project"]
collection = db["tweets_spark"]

# Class label mapping
class_index_mapping = {0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant"}

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .master("local[*]") \
    .getOrCreate()

# UDF to clean tweet text
def clean_text(text):
    if text:
        text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
        text = re.sub(r'(@|#)\w+', '', text)
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ''

clean_text_udf = udf(clean_text, StringType())

# Kafka consumer setup (standalone from Spark)
consumer = KafkaConsumer(
    'numtest',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='spark-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

# Process messages from Kafka
for message in consumer:
    try:
        tweet_raw = message.value[-1]
        tweet_cleaned = clean_text(tweet_raw)
        tweet_vector = vectorizer.transform([tweet_cleaned])
        prediction = model.predict(tweet_vector)[0]
        sentiment = class_index_mapping.get(int(prediction), "Unknown")

        print(f"-> Tweet: {tweet_raw}")
        print(f"-> Cleaned: {tweet_cleaned}")
        print(f"-> Sentiment: {sentiment}")
        print("/" * 50)

        # Insert into MongoDB
        doc = {"tweet": tweet_raw, "prediction": sentiment}
        collection.insert_one(doc)

    except Exception as e:
        print("❌ Error:", e)

