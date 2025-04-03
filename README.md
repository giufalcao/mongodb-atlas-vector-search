# MongoDB Atlas Vector Search

This repository demonstrates how to perform **vector search** using **MongoDB Atlas**. It provides an example of integrating vector embeddings with MongoDB's search capabilities for efficient similarity search.

This project was created to address the [Atlas Vector Search Overview](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) and includes code examples and tutorials.

Additionally, this repository was designed to execute the **Quick Start** tutorials offered by MongoDB. The goal is to have a well-structured repository that allows the following operations via code:

1. **Data Processing**
2. **Embedding Generation**
3. **Storing Embeddings in Atlas**
4. **Querying Relevant Documents Based on User Input**

---

## 🚀 Features

- **Connect** and **interact** with MongoDB Atlas using Python.
- **Create** an Atlas Search `search_index` by defining `vectorSearch`.
- **Run** a Vector Search Query using `$vectorSearch` aggregation.
- **Efficient Similarity Search** with embeddings.
- **Example Dataset**: Includes `sample_airbnb` for testing.
- **Collection Used**: `listingsAndReviews`

---

## 📋 Prerequisites

### ✅ Local Tools

Ensure you have the following tools installed:

| Tool      | Version  | Purpose | Installation Link |
|----------|---------|---------|------------------|
| Python   | 3.12    | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv       | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-bash/uv) |

### ☁️ Cloud Services

The project requires access to **MongoDB Atlas**. Authentication is handled via environment variables in the `.env` file.

| Service | Purpose | Cost | Environment Variable | Setup Guide |
|---------|---------|------|---------------------|-------------|
| [MongoDB Atlas](https://rebrand.ly/second-brain-course-mongodb) | Document database (with vector search) | Free tier | `MONGODB_URI` | [Setup Guide](https://www.mongodb.com/cloud/atlas/register?utm_campaign=ai-pilot&utm_medium=creator&utm_term=iusztin&utm_source=course) |

---

## ⚡ Setup Instructions

1. **Set up your Atlas Cluster:** Follow the [official guide](https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/vector-search-quick-start/).

2. **Clone this repository:**
   ```bash
   git clone https://github.com/giufalcao/mongodb-atlas-vector-search.git
   cd mongodb-atlas-vector-search
   ```

3. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv <name-of-your-env>
   source ./.<name-of-your-env>/bin/activate  # or ./.<name-of-your-env>/bin/activate
   uv pip install -e .
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Set your **MongoDB connection string** in `.env`:
     ```bash
     MONGODB_URI="your-mongodb-uri"
     DB_NAME="vector_db"
     COLLECTION_NAME="embeddings"
     ```

---

## 🎯 Usage

1. **Run the pipeline:**
   ```bash
   python src/main.py
   ```
---

## 🛠️ Troubleshooting

If you run into issues, here are some common solutions:

### 1. `ModuleNotFoundError: No module named 'src'`
   **Solution:** Ensure you are running the script from the root directory of the project:
   ```bash
   python -m src.ingest
   ```

### 2. `pymongo.errors.ServerSelectionTimeoutError`
   **Solution:** Check if:
   - Your **MongoDB Atlas cluster** is active.
   - The **MONGODB_URI** in `.env` is correctly set.
   - You have **whitelisted your IP** in MongoDB Atlas security settings.

### 3. `KeyError: 'search_score'`
   **Solution:** This likely means the vector search is not returning expected results. Try:
   - Ensuring **indexes** are properly set up in MongoDB Atlas.
   - Checking if embeddings were successfully stored in the database.

### 4. **Some Features May Not Work on MongoDB Atlas Free Tier**
   **Issue:** Certain capabilities, such as **vector search on large datasets** or **advanced indexing**, may not be available on the **Free Tier** of MongoDB Atlas.
   **Solution:** Consider upgrading to a **paid tier** for full access to all vector search features.

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## 📜 License

This project is licensed under the **MIT License**.
