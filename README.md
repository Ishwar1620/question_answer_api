# Question-Answer API

Simple production-ready Question-Answer API with vector search and LLM generation.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://user:{pass_word}@localhost:5432/dbname
DATABASE_PASS=your_password
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=qa_hybrid
PINECONE_CLOUD=aws
PINECONE_REGION=us-east1
GEMINI_API_KEY=your_gemini_key
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /ask` - Ask a question
- `GET /health` - Health check
- `GET /docs` - API documentation

## Example Request

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the user name?"}'
```

## Response

```json
{
  "answer": "Based on the available data..."
}
```
