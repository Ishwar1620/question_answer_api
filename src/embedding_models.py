from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder
import numpy as np
import os

class EmbeddingManager:
    def __init__(self,dense_model_name: str = 'all-MiniLM-L6-V2'):
        self.dense_model_name = dense_model_name
        self.sparse_model = BM25Encoder()
        self.model = None
        self._load_dense_model()
    
    def _load_dense_model(self):
        try:
            print(f"Loading Dense Embedding Model {self.dense_model_name}")
            self.model = SentenceTransformer(self.dense_model_name)
            print(f"Model {self.dense_model_name} loaded sucessfully with embeddings dimentions of {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error {e} Model {self.dense_model_name} Load Failed")

    def get_dense_embedding(self,texts:list[str])-> np.array:
        if not self.model:
            raise ValueError(f"Model {self.model} not loaded ")
        # Handle both string and list inputs
   
        print(f"Genrating embbeding for {len(texts)} ...")
        embeddings = self.model.encode(texts,show_progress_bar=False)
        print(f"Embeddings are Genrated with shape {embeddings.shape}")
        # Return single embedding if input was string
       
        return embeddings
    
    def get_sparse_embedding(self,texts:list[str]) -> dict:
        if not self.sparse_model:
            raise ValueError(f"Model {self.sparse_model} loading failed")
        # Handle both string and list inputs
        print(f"Generating embedding for {len(texts)}...")
        self.sparse_model.fit(texts)
        sparse_embeddings = self.sparse_model.encode_documents(texts)
        print(f"Embeddings are genrated!")
        # Return single embedding if input was string
        return sparse_embeddings