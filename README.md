
# 🐦 Real-Time Twitter Sentiment Analysis

This project performs **real-time sentiment analysis** on live Twitter data using **Apache Kafka**, **Apache Spark**, and **PySpark ML**. It streams tweets, processes them using a trained machine learning model, and displays sentiment predictions (positive, negative, neutral) in real-time.

---

## 🚀 Project Features

- ✅ Real-time tweet streaming using Tweepy & Twitter API v2
- ✅ Apache Kafka for distributed message ingestion
- ✅ Apache Spark Streaming for processing and inference
- ✅ ML pipeline using PySpark (Tokenizer, TF-IDF, Logistic Regression)
- ✅ Visual dashboard (optional via Streamlit or Plotly)
- ✅ Deployable on local machine or cloud

---

## 🧱 Tech Stack

| Component       | Technology           |
|----------------|----------------------|
| Language        | Python 3.x           |
| Data Streaming  | Apache Kafka         |
| Processing      | Apache Spark + PySpark |
| ML Model        | Spark ML Pipeline    |
| Data Source     | Twitter API (Tweepy) |
| Packaging       | Docker (optional)    |

---

## 📂 Project Structure

```
Real-Time-Twitter-Sentiment-Analysis/
├── Kafka-PySpark/                 # Spark Streaming consumer
│   └── tweet_consumer.py
├── ML PySpark Model/             # Model training & CSV data
│   ├── train_model.py
│   ├── run_model_local.py
│   ├── twitter_training.csv
│   └── sentiment_model/         # Saved PySpark PipelineModel
├── Django-Dashboard/             # Optional UI (future)
├── zk-single-kafka-single.yml    # Docker Compose for Kafka & Zookeeper
└── requirements.txt
```

---

## 🧪 How to Run the Project

### 1. ✅ Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure Java 11+ and Spark are installed and configured.

### 2. ✅ Train the Model (or use pretrained)

```bash
cd "ML PySpark Model"
python train_model.py
```

This will generate a `sentiment_model/` folder.

### 3. ✅ Start Kafka and Zookeeper

```bash
docker compose -f zk-single-kafka-single.yml up
```

### 4. ✅ Run Twitter Stream Producer

```bash
python twitter_producer.py
```

This sends live tweets to a Kafka topic.

### 5. ✅ Run Spark Consumer

```bash
python Kafka-PySpark/tweet_consumer.py
```

This consumes the tweets, predicts sentiment, and prints the output.

---

## 📊 Sample Output

```
Tweet: "I love the new iPhone!"
Sentiment: Positive (0.0)

Tweet: "This is the worst update ever..."
Sentiment: Negative (1.0)
```

---

## ⚙️ Model Details

- Preprocessing: Tokenizer, StopWordsRemover, HashingTF, IDF
- Classifier: Logistic Regression
- Training Data: Cleaned from `twitter_training.csv`

---

## 📝 To-Do / Improvements

- [ ] Improve classification with deep learning models (BERT, RoBERTa)
- [ ] Add visualization dashboard (Streamlit)
- [ ] Enable multi-language tweet support
- [ ] Deploy on cloud (AWS/GCP/Azure)

---

## 🙌 Contributors

- **Mitali Trivedi**
- **Kazi Afroz Alam**
- **Mateen Khan**
- **Ranjit Kumar Behera**

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
