# 🔍 Redis-Based BM25 Search Engine

A lightweight, full-text search engine built with Python and Redis, powered by the **BM25 (Best Matching 25)** ranking algorithm. This project crawls web content, indexes it into Redis, and serves ranked search results through a web interface.

---

## 🧠 How It Works

BM25 is a probabilistic ranking function that scores documents based on how relevant they are to a search query. It improves on classic TF-IDF by accounting for:

- **Term frequency saturation** — repeated keywords don't over-inflate scores
- **Document length normalization** — shorter documents aren't unfairly penalized

This project combines BM25 scoring with Redis as a fast in-memory index store, enabling millisecond-latency search over crawled document collections.

---

## 📁 Project Structure

```
├── microsearch/         # Core search library (BM25 engine + indexing logic)
├── templates/           # HTML templates for the web UI
├── crawl.py             # Web crawler — fetches and parses documents
├── crawl_redis.py       # Indexes crawled documents into Redis
├── main.py              # Web server / search API entry point
├── data.csv             # Sample dataset of crawled documents
├── pyproject.toml       # Project dependencies and metadata
└── .python-version      # Python version pin
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A running [Redis](https://redis.io/docs/getting-started/) instance

```bash
# Start Redis locally (macOS/Linux)
redis-server
```

### Installation

```bash
git clone https://github.com/sayantancodex/Redis-Based-BM25-Search-Engine.git
cd Redis-Based-BM25-Search-Engine

pip install .
```

### Usage

**1. Crawl documents:**
```bash
python crawl.py
```

**2. Index into Redis:**
```bash
python crawl_redis.py
```

**3. Start the search server:**
```bash
python main.py
```

Then open your browser and visit `http://localhost:5000` (or whichever port is configured).

---

## 🛠️ Tech Stack

| Component     | Technology        |
|---------------|-------------------|
| Ranking       | BM25 (Okapi)      |
| Index Store   | Redis             |
| Web Framework | Python (Flask/FastAPI) |
| Crawler       | Python            |
| Templating    | Jinja2 / HTML     |

---

## 📖 Background

BM25 (Best Matching 25) is the ranking algorithm behind major search engines like **Elasticsearch** and **Apache Lucene**. It was developed at City University London in the 1990s and remains the gold standard for keyword-based document retrieval.

Key parameters:
- `k1` — controls term frequency saturation (default: `1.2`)
- `b` — controls document length normalization (default: `0.75`)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source. Check the repository for license details.
