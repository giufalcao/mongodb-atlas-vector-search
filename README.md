# MongoDB Atlas Vector Search

This repository demonstrates how to perform vector search using MongoDB Atlas. It provides an example of integrating vector embeddings with MongoDB's search capabilities for efficient similarity search.

This repository was created to address the [Atlas Vector Search Overview](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) and its code examples and tutorials.

## Features

- Connect and interact with MongoDB Atlas using Python
- Create a Atlas Search, `search_index`, by defining `vectorSearch`
- Run a Vector Search Query
- Connect and interact with MongoDB Atlas using Python
- Implement vector search via `$vectorSearch` aggregation
- Example dataset and queries for testing with sample_mflix

## 📋 Prerequisites

### Local Tools

For all the modules, you'll need the following tools installed locally:

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| Python | 3.12 | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-sh/uv) |

### Cloud Services

The project requires access to the following cloud services. Authentication is handled via environment variables in the `.env` file:

| Service | Purpose | Cost | Environment Variable | Setup Guide |
|---------|---------|------|---------------------|-------------|
| [OpenAI API](https://openai.com/index/openai-api/) | LLM API | Pay-per-use | `OPENAI_API_KEY` | [Quick Start Guide](https://platform.openai.com/docs/quickstart) |
| [MongoDB](https://rebrand.ly/second-brain-course-mongodb) | Document database (with vector search) | Free tier | `MONGODB_URI` | [Setup Guide](https://www.mongodb.com/cloud/atlas/register?utm_campaign=ai-pilot&utm_medium=creator&utm_term=iusztin&utm_source=course) |

## Setup

1. Set up your [Atlas Cluster](https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/vector-search-quick-start/):

2. Clone this repository:
   ```sh
   git clone https://github.com/giufalcao/mongodb-atlas-vector-search.git
   cd mongodb-atlas-vector-search
   ```

3. Create a virtual environment and install dependencies using `uv`:
   ```sh
   uv venv
   uv pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` and update the values:
     ```sh
     cp .env.example .env
     ```
   - Set your MongoDB connection string in `.env`:
     ```sh
     MONGO_URI="your-mongodb-uri"
     DB_NAME="vector_db"
     COLLECTION_NAME="embeddings"
     OPENAI_API_KEY="your-openai-api-key"
     ```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

