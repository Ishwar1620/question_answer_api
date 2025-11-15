from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.retrieval_generation import RetrievalGenration
from src.embedding_models import EmbeddingManager
from src.vectorstore import VectorStore


class QAService:
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding = EmbeddingManager()
    
    async def get_user_id(
        self,
        db: AsyncSession,
        question: str
    ) -> Optional[str]:
        """
        Get user ID from question using similarity search.
        
        Args:
            db: Database session
            question: The question string
            
        Returns:
            User ID if found, None otherwise
        """
        try:
            sql = text("""
                SELECT user_id, similarity(user_name, :q) as score
                FROM qa_db.users
                WHERE similarity(user_name, :q) > 0.10
                ORDER BY score DESC
                LIMIT 1
            """)
            result = (await db.execute(sql, {'q': question})).mappings().first()
            
            if result:
                return str(result['user_id'])
            
            return None
            
        except Exception:
            return None
    
    async def get_answer(
        self,
        question: str,
        user_id: Optional[str] = None
    ) -> dict[str, str]:
        """
        Get answer for a question.
        
        Args:
            question: The question to answer
            user_id: Optional user ID to filter results
            
        Returns:
            Dictionary with answer
        """
        try:

            if not self.vector_store.index:
                raise ValueError("Vector store index is not initialized. Check Pinecone configuration.")
            

            if not self.embedding.model:
                raise ValueError("Embedding model is not loaded. Check model initialization.")
            
            retgen = RetrievalGenration(
                self.vector_store,
                self.embedding,
                question,
                user_id
            )
            
            result = await retgen.main()
            
            if not result :
                return {
                    "answer": "Answer cannot be determined from the available data."
                }
            
            return result
            
        except Exception as e:
            
            return {
                "answer": f"An error occurred: {type(e).__name__}: {str(e)}"
            }

