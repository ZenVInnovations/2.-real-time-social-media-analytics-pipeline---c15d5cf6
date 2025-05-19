from pyspark.sql import SparkSession
print("🟢 Starting Spark session...")
spark = SparkSession.builder.appName("TestSpark").getOrCreate()
print("✅ Spark session started successfully.")
df = spark.createDataFrame([(1, "hello"), (2, "world")], ["id", "text"])
df.show()
