## Movie Recommendation System - Submission Report

Author: [Your Name]
Date: November 11, 2025
Repository: `main-project-for-aiml-main`

### 1) Abstract
This project implements a movie recommendation system with data ingestion, cleaning, feature enrichment, model-based and heuristic recommenders, and a lightweight web app for interactive exploration. The pipeline supports both baseline and enhanced variants, and includes an IMDb scraper for optional data augmentation.

### 2) Objectives
- Build an end-to-end reproducible pipeline for movie recommendations.
- Compare baseline and enhanced data processing and recommendation strategies.
- Provide an interactive web interface for recommendations and browsing.

### 3) System Overview
The system is organized around a linear data-to-app pipeline:
1) Data acquisition (local datasets and optional IMDb scraping).
2) Data cleaning and enrichment (feature engineering).
3) Recommendation generation (baseline and enhanced strategies).
4) Web application for serving recommendations.

#### Flowchart (High-Level Workflow)
```mermaid
flowchart TD
    A[Start] --> B[Load Raw Data<br/>(local CSV / IMDb Scraper)]
    B --> C[Data Cleaning<br/>src/data_processing.py]
    C --> D[Feature Enrichment<br/>src/enhanced_data.py]
    D --> E{Choose Recommender}
    E -->|Baseline| F[Baseline Recs<br/>src/recommendation.py]
    E -->|Enhanced| G[Enhanced Recs<br/>src/enhanced_recommendation.py]
    F --> H[Serve via Web App<br/>src/web_app.py / src/clean_web_app.py]
    G --> H
    H --> I[Enhanced Web App (Optional)<br/>src/enhanced_web_app.py]
    I --> J[User Interaction<br/>query, filter, explore]
    J --> K[End]
```

### 4) Data Acquisition
- Local data: Loaded through utilities in `src/data_processing.py` and related modules.
- Optional scraping: `src/imdb_scraper.py` can augment the dataset with metadata (ratings, genres, cast).

Inputs are validated and standardized to ensure downstream compatibility (e.g., consistent types, missing value handling).

### 5) Data Cleaning and Enrichment
- Cleaning (`src/data_processing.py`):
  - Handle duplicates and missing values.
  - Normalize text fields (titles, genres).
  - Standardize numeric ranges (ratings, votes, runtime).
- Enrichment (`src/enhanced_data.py`):
  - Feature engineering for content-based similarity (e.g., bag-of-words/TF‑IDF style genre and overview embeddings, normalized numeric signals).
  - Optional joins with scraped attributes.

### 6) Recommendation Strategies
- Baseline (`src/recommendation.py`):
  - Simple similarity and/or popularity heuristics.
  - Useful as a minimum viable product for quick results.
- Enhanced (`src/enhanced_recommendation.py`):
  - Content-based recommendations leveraging engineered features.
  - Better personalization and diversity options compared to baseline.

Both strategies are designed to operate on the cleaned/enriched artifacts to keep data concerns separate from modeling.

#### Main Algorithm (Enhanced Content-Based Recommender)

- Core idea: represent each movie as a feature vector built from text (e.g., genres, overview, keywords) and numeric signals (e.g., rating, votes, year), then recommend items that are most similar to a user’s query item or profile using cosine similarity. A small popularity smoothing term prevents overly niche results when features are sparse.

- Feature construction:
  - Textual features: TF‑IDF or similar vectorization on concatenated text fields (genres, overview, tags).
  - Numeric features: scaled to zero mean and unit variance (ratings, vote counts, runtime, year).
  - Final vector: concatenation of normalized text and numeric vectors with optional weights.

- Similarity:
  - Cosine similarity between movie vectors \(v_i, v_j\): \(\text{cos\_sim}(i,j) = \frac{v_i \cdot v_j}{\|v_i\| \, \|v_j\|}\).

- Ranking with popularity smoothing:
  - Let \(p_j\) be normalized popularity (e.g., log(votes) rescaled to \([0,1]\)).
  - Final score: \(\text{score}(i \rightarrow j) = \alpha \cdot \text{cos\_sim}(i,j) + (1-\alpha) \cdot p_j\), with \(\alpha \in [0,1]\).

- Diversity (optional):
  - Re-rank top‑N with Maximal Marginal Relevance (MMR) to reduce redundancy: \(\text{MMR} = \arg\max_{d \in C \setminus S} \lambda \cdot \text{rel}(d) - (1-\lambda) \max_{s \in S} \text{sim}(d,s)\).

- Complexity:
  - Offline vectorization: depends on vocabulary size \(V\) and items \(M\); typical TF‑IDF is \(O(\text{nnz})\) where \(\text{nnz}\) is non-zeros.
  - Online recommendation (naive): \(O(M \cdot d)\) per query, where \(d\) is vector dimension. For large \(M\), use approximate nearest neighbors (e.g., Faiss/Annoy/HNSW).

- Key parameters:
  - \(\alpha\) (similarity vs popularity), text vs numeric feature weights, TF‑IDF min_df/max_df, top‑K candidate pool before re‑ranking, MMR \(\lambda\).

Example pseudocode:

```python
def prepare_item_vectors(items, text_fields, numeric_fields, weights):
    # Fit TF-IDF on concatenated text; scale numeric; concatenate with weights
    tfidf = TfidfVectorizer(min_df=2, max_df=0.9, ngram_range=(1,2))
    text_corpus = [concat_text_fields(x, text_fields) for x in items]
    X_text = tfidf.fit_transform(text_corpus)  # shape: (M, V)

    X_num = scale_numeric_matrix(items, numeric_fields)  # shape: (M, K)
    X = hstack([weights["text"] * X_text, weights["num"] * X_num])  # sparse ok

    popularity = normalize(log1p(items["vote_count"]))  # in [0,1]
    return X, popularity, tfidf

def recommend_for_item(item_idx, X, popularity, top_n=10, alpha=0.9):
    q = X[item_idx]  # sparse row
    sims = cosine_similarity(q, X).ravel()  # vector of length M
    scores = alpha * sims + (1 - alpha) * popularity
    scores[item_idx] = -inf  # avoid self
    top = np.argpartition(scores, -max(100, top_n))[-max(100, top_n):]
    top = top[np.argsort(scores[top])[::-1]]
    return top[:top_n]
```

Baseline variant:
- Use a smaller, text-only vector (genres/keywords) or even a popularity-only ranking.
- Complexity is reduced; quality may drop for niche items.

### 7) Web Applications
- Clean app (`src/clean_web_app.py` / `src/web_app.py`):
  - Minimal interface to request and display recommendations.
  - Fast to launch for sanity checks and demos.
- Enhanced app (`src/enhanced_web_app.py`):
  - Additional UI affordances and possibly richer filters.

Launch helpers are provided:
- Windows PowerShell: `.\run_project.ps1`
- Windows CMD/Batch: `run_project.bat`
- Direct module/script execution paths are available via the `src/` modules.

#### App UI Workflow (Streamlit)
The Streamlit web interface guides users from setting preferences to viewing recommendations and analyses.

```mermaid
graph TD
    A[Start: User opens the web app] --> B{Load Recommendation System};
    B --> C[Display Main UI: Header, Sidebar, and Main Content Area];

    subgraph "User Interaction in Sidebar"
        D[Select Favorite Genres]
        E[Enter Favorite Actors]
        F[Enter Favorite Directors]
        G[Adjust Recommendation Settings: Number of movies, weights]
    end

    C --> D;
    C --> E;
    C --> F;
    C --> G;

    subgraph "Main Content Actions"
        H[Click "Get Recommendations" button]
        I[Select a movie and click "Find Similar"]
        J[Select a genre and click "Get Top Movies"]
    end

    C --> H;
    C --> I;
    C --> J;

    H --> K{User Preferences Provided?};
    K -- Yes --> L[Get Personalized Recommendations];
    K -- No --> M[Show Error: "Please select at least one genre"];

    L --> N[Display Recommended Movies with details];
    L --> O[Display User's "Taste Analysis"];

    I --> P[Find and Display Similar Movies];
    J --> Q[Find and Display Top Movies for the Genre];

    subgraph "Recommendation Engine"
        L -- uses --> R(recommender.get_recommendations)
        P -- uses --> S(recommender.get_similar_movies)
        Q -- uses --> T(recommender.get_genre_recommendations)
    end

    N --> U[End];
    O --> U;
    P --> U;
    Q --> U;
    M --> U;
```

Key UI steps:
- Initialization: load data and prepare the recommender.
- Sidebar inputs: genres, actors, directors, and weighting/quantity controls.
- Main actions: personalized recommendations, similar movies, top movies by genre.
- Outputs: ranked lists with details and a simple “taste analysis” summary.

### 8) How to Run
1) Environment
   - Python: See `requirements.txt` for dependencies.
   - Install deps: `pip install -r requirements.txt`
2) Quick Start
   - Windows (PowerShell): `.\run_project.ps1`
   - Windows (CMD): `run_project.bat`
   - Or run a specific app, for example:
     - `python -m src.web_app`
     - `python -m src.enhanced_web_app`
3) Optional: Scrape IMDb
   - `python -m src.imdb_scraper` (respect robots.txt and rate limits).

### 9) Testing and Validation
- Basic system tests live in `test_system.py` and notebooks under `notebooks/` (e.g., `movie_analysis.ipynb`) for exploratory evaluation.
- Sanity checks: dataset cardinality, missing value rates, and recommendation coverage.

### 10) Results (Example Outline)
- Baseline: High speed, reasonable top‑N accuracy on popular titles, lower personalization.
- Enhanced: Improved relevance/diversity for niche titles; minor latency overhead.

Note: Concrete metrics depend on the final dataset snapshot and evaluation protocol. For submission, include top‑N precision/recall or MAP@K where possible.

### 11) Limitations and Future Work
- Collaborative filtering variants (user–item interactions) are not included by default.
- Cold start remains challenging without richer metadata or user profiling.
- Future: Hybrid models, lightweight embeddings, and A/B testing in the web app.

### 12) Repository Map (Key Files)
- `src/data_processing.py`: Core cleaning pipeline.
- `src/enhanced_data.py`: Feature engineering/enrichment.
- `src/recommendation.py`: Baseline recommendation logic.
- `src/enhanced_recommendation.py`: Enhanced/content-based recommendations.
- `src/web_app.py`, `src/clean_web_app.py`, `src/enhanced_web_app.py`: App entry points.
- `src/imdb_scraper.py`: Optional scraping utility.
- `test_system.py`: Basic tests.
- `notebooks/movie_analysis.ipynb`: Exploratory data analysis.

### 13) Conclusion
The project demonstrates a clear, modular pathway from raw movie data to deployable recommendation endpoints with an interactive UI. The separation of concerns between data preparation, recommendation logic, and UI allows straightforward experimentation and future improvements.


