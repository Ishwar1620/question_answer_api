from dotenv import load_dotenv
import os

load_dotenv()

# Database
DATABASE_URL = os.getenv('DATABASE_URL', '')
DATABASE_PASS = os.getenv('DATABASE_PASS', '')
if DATABASE_PASS and '{pass_word}' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.format(pass_word=DATABASE_PASS)

# Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', '')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'qa_hybrid')
cloud = os.getenv('PINECONE_CLOUD', 'aws')
region = os.getenv('PINECONE_REGION', 'us-east1')

# Gemini
gemini_key = os.getenv('gemini_api_key', '')

# External API (optional)
public_data_url = os.getenv('MEMBER_DATA_PUBLIC_API', '')
data_api_param = {
    'skip': int(os.getenv('DATA_API_SKIP', '0')),
    'limit': int(os.getenv('DATA_API_LIMIT', '3349'))
}

# For backward compatibility
pc_api_key = PINECONE_API_KEY
pc_index_name = PINECONE_INDEX_NAME
pinecone_index_name = PINECONE_INDEX_NAME
database_url = DATABASE_URL
database_pass = DATABASE_PASS
