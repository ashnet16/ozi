# Ozi 🧠📡

**Ozi** is an open-source real-time analytics and RAG (Retrieval-Augmented Generation) engine for [Farcaster](https://www.farcaster.xyz).

It ingests Casts, embeds them with local LLMs, and makes them queryable via semantic search or SQL. Built to power Farcaster-native apps, dashboards, and intelligent agents.

Note: This is polling from a self hosted Hub.

---

## ⚙️ Architecture

- **Kafka / MSK** – event streaming for Farcaster + onchain data
- **FastAPI** – API for queries (LLM + SQL)
- **DuckDB** – local analytics engine for fast querying
- **Vector DB** – semantic search layer (FAISS or Chroma)
- **Local LLMs** – embed + retrieve context-aware responses

---

## 🧪 Use Cases (WIP)

- Query Casts via natural language
- Run custom analytics on Farcaster events
- Build dashboards or agents over social data
- Warpcast-integrated search and summarization

---

## 🛠️ Project Status

> Ozi is in early WIP. We’re building in public and welcoming feedback.

- ✅ Kafka ingestion
- ✅ Embedder master for LLM-based indexing
- ✅ Query API (FastAPI)
- 🧩 Analytics / dashboarding
- 🧩 Warpcast frame integration
- 🧩 Token/gov idea experiments

---

## 🚀 Getting Started

#### 1. Clone and install dependencies

```bash
git clone https://github.com/ashnet16/ozi.git
cd ozi
pip install -r requirements.txt
```

#### 2. Spin up Kafka

``` docker compose up -d

```

#### 3. Run the Farcaster Poller

```
python3 -m producers.pollers
```
#### 4. Start the Consumer Service

```
python3 -m consumers.consumers
```


#### Below are the Kafka Topics

```
kafka-topics --bootstrap-server localhost:9092 \
  --create --topic farcaster.cast.add --partitions 1 --replication-factor 1

kafka-topics --bootstrap-server localhost:9092 \
  --create --topic farcaster.events.other --partitions 1 --replication-factor 1

kafka-topics --bootstrap-server localhost:9092 \
  --create --topic farcaster.events.dlq --partitions 1 --replication-factor 1
```

#### Consume inside the container


```
kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic farcaster.events.add \
  --from-beginning \
  --property print.key=true \
  --property print.value=true

```
