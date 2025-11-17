# Question-Answer API

Simple Question-Answer API.

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
PINECONE_INDEX_NAME=index_name
PINECONE_CLOUD=cloud
PINECONE_REGION=us region
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
## Application live on

(https://qaapiservice-fag4dnfkakg2hnad.canadacentral-01.azurewebsites.net/docs)

