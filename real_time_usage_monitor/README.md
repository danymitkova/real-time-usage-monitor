
# Real‑Time Product Usage Monitor

End‑to‑end showcase of a streaming analytics stack:

* **Kafka → Spark Structured Streaming → Delta Lake**
* **AI anomaly detection** (scikit‑learn Isolation Forest)
* **Live dashboard** (Streamlit)
* **dbt models** + data‑quality tests
* CI pipeline with pytest & GitHub Actions

> **Note**: all data is synthetic, generated on the fly by `data_simulator/`.

---

## 📐 Architecture

```mermaid
graph TD
    A[Data simulator<br>(Python + Faker)] -->|JSON events| K(Kafka topic)
    K --> S(Spark Structured Streaming)
    S --> D[Delta Lake<br>silver & gold]
    D --> B[dbt models]
    D --> ST[Streamlit dashboard]
    B -->|tests| CI(CI GitHub Actions)
```

---

## 🚀 Quick start (local demo)

```bash
# 1) spin up Kafka + Spark (docker compose)
docker compose up -d

# 2) start event generator
python data_simulator/simulate_events.py

# 3) run streaming job (in new terminal)
python spark_app/streaming_job.py

# 4) launch dashboard
streamlit run streamlit_app.py
```

---

## Repo layout

```
data_simulator/         # event generator (writes to Kafka or CSV fallback)
spark_app/              # PySpark Structured Streaming job
streamlit_app.py        # real‑time KPI & anomaly feed
dbt_demo_project/       # minimal dbt skeleton
notebooks/
└── anomaly_exploration.ipynb
tests/                  # pytest data‑quality checks
.github/workflows/ci.yml
requirements.txt
docker-compose.yml
```

---

## ⚙️ Tech versions

* Python 3.10
* Kafka 3.x (Redpanda quickstart)
* Apache Spark 3.4 (pyspark)
* Delta 2.x
