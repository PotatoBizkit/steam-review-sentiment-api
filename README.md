# Steam Review Sentiment API

A production-style sentiment analysis API for Steam game reviews, built end-to-end as a learning project covering the modern ML backend stack: model training, API serving, persistence, caching, containerization, and CI.

Given a piece of review text, the API predicts whether it reflects a "Recommended" or "Not Recommended" sentiment, along with a confidence score — served over REST, cached in Redis, and logged to PostgreSQL.

## Tech Stack

- **Language:** Python
- **ML:** scikit-learn (TF-IDF + Logistic Regression)
- **API:** FastAPI, Pydantic
- **Database:** PostgreSQL (via SQLAlchemy)
- **Cache:** Redis
- **Containerization:** Docker, Docker Compose
- **Data/Model Versioning:** DVC
- **CI:** GitHub Actions
- **Experimentation:** Jupyter Notebook

## Project Structure

```text
sentiment-api/
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── database.py              # SQLAlchemy engine/session setup
│   ├── redis_client.py          # Redis connection setup
│   ├── models/                  # SQLAlchemy DB models + trained model artifacts
│   ├── routers/                 # API route definitions
│   └── schemas/                 # Pydantic request/response schemas
├── notebooks/
│   └── train_model.ipynb        # Data prep + model training
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions build/import checks
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .dvc/                        # DVC config (dataset + model tracked)
```

## Dataset

Steam reviews scraped for 18 games (~132K reviews after cleaning), covering titles like Elden Ring, Cyberpunk 2077, The Witcher 3, Counter-Strike 2, and others. Reviews are labeled by Steam's own "Recommended / Not Recommended" tag.

The dataset and trained model (`.pkl` files) are tracked with **DVC**, not committed directly to Git. To use them:
- Regenerate them yourself by running `notebooks/train_model.ipynb` end to end, using your own Steam review data.

## Getting Started

### Option A: Run with Docker (recommended)

1. Clone the repo:
```bash
   git clone https://github.com/PotatoBizkit/steam-review-sentiment-api.git
   cd steam-review-sentiment-api
```

2. Copy the example environment file and fill in your own values:
```bash
   cp .env.example .env
```
   You'll need to set your own PostgreSQL and Redis credentials.

3. Make sure you have a trained model available at `app/models/sentiment_model.pkl` and `app/models/tfidf_vectorizer.pkl` (see [Dataset](#dataset) above — run the notebook if you don't have DVC remote access).

4. Build and start everything:
```bash
   docker compose up --build
```

5. Visit the interactive API docs:
   http://127.0.0.1:8000/docs


### Option B: Run locally without Docker

1. Create a virtual environment and install dependencies:
```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

2. Install and run PostgreSQL and Redis locally (or via your own Docker containers), and configure `.env` with `localhost`-based connection strings.

3. Run the model training notebook (`notebooks/train_model.ipynb`) to generate `sentiment_model.pkl` and `tfidf_vectorizer.pkl` in `app/models/`.

4. Start the API:
```bash
   fastapi dev app/main.py
```

## API Reference

### `POST /sentiment/predict`

**Request body:**
```json
{
  "review_text": "This game is amazing, best purchase ever"
}
```

**Response:**
```json
{
  "review_text": "This game is amazing, best purchase ever",
  "recommendation": true,
  "confidence": 0.93
}
```

Full interactive documentation (Swagger UI) is available at `/docs` once the server is running.

## How It Works

1. Incoming review text is hashed to generate a cache key.
2. **Redis** is checked first — if this exact text was predicted recently (within the last hour), the cached result is returned immediately.
3. On a cache miss, the text is vectorized with a pre-trained **TF-IDF** vectorizer and passed to a **Logistic Regression** model for prediction.
4. The result is cached in Redis (1-hour TTL) and logged to **PostgreSQL**.
5. The prediction is returned to the caller.

## Model Details

- **Vectorization:** TF-IDF (10,000 features, English stop words removed)
- **Classifier:** Logistic Regression (`class_weight="balanced"` to handle class imbalance — the dataset skews heavily toward "Recommended" reviews)
- **Evaluation:** See `notebooks/train_model.ipynb` for the full classification report and confusion matrix

## CI

Every push to `main` triggers a GitHub Actions workflow that installs dependencies and verifies the app imports and builds correctly. See `.github/workflows/ci.yml`.

> **Note:** the CI pipeline currently does not pull the trained model from the DVC remote (this requires non-interactive service-account authentication, not yet configured), so the import/build check may fail on model-loading — a known, documented limitation.

## Environment Variables

See `.env.example` for the full list. At minimum, you'll need:
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<dbname>
REDIS_URL=redis://<host>:6379/0


When running via Docker Compose, use `db` and `redis` as the hostnames (Docker's internal service names). When running locally, use `localhost`.

## Future Improvements

- Non-interactive DVC remote auth (service account) for full CI/CD model pulling
- Rate limiting on the `/predict` endpoint
- Model retraining pipeline / experiment tracking (MLflow or W&B)
- Authentication (JWT) for protected endpoints
- Cloud deployment

## License

MIT
