from src.embedding_models import EmbeddingManager
from pinecone import Pinecone,ServerlessSpec
from dotenv import load_dotenv
from settings import config
import numpy as np
import uuid
import os
load_dotenv()

class VectorStore:
    def __init__(self):
        self.index = config.pc_index_name
        self.api_key  =config.pc_api_key
        self.MAX_BATCH_SIZE = 96
        self.pc_vector_store=None
        self._initialize_store()

    def _initialize_store(self):
        print(f"Authenticating Vector DB..")
        try:
            if not self.api_key:
                raise ValueError("PINECONE_API_KEY is not set in environment variables")
            
            self.pc_vector_store = Pinecone(api_key=self.api_key)
            print(f"API key authenticate sucessfully")
            
            index_name = self.index
            existing_indexes = [i['name'] for i in self.pc_vector_store.list_indexes()]
            
            if index_name not in existing_indexes:
                print(f"Index {index_name} not found, creating new index...")
                # Get embedding dimension from model
                embedding_manager = EmbeddingManager()
                dimension = embedding_manager.model.get_sentence_embedding_dimension() if embedding_manager.model else 384
                self.pc_vector_store.create_index(
                    name = index_name,
                    dimension = dimension,
                    metric= 'dotproduct',
                    spec= ServerlessSpec(
                        cloud=config.cloud,
                        region=config.region
                    )
                )
                print(f"Index {index_name} created successfully")
            
            self.index = self.pc_vector_store.Index(index_name)
            print(f"Vector store set up complete. Index: {index_name}")
        except Exception as e:
            print(f"Vector Store Initialization Failed Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            self.index = None
              

    def add_documents(self,documents:list[any],dense_embeddings:np.array,sparse_embeddings:list):
        if len(documents) != len(dense_embeddings):
            print(f"Number of Documents not matching no of embeddings")
        print(f"Adding {len(documents)} to vector store...")
        database=[]
        for i,(chunk,dense_embedding,sparse_embedding) in enumerate(zip(documents,dense_embeddings,sparse_embeddings)):
            doc_id  = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            data = {
                'id': doc_id,
                'values': dense_embedding,
                'sparse_values':sparse_embedding,
                'metadata': {
                    'text':chunk.page_content,
                    **chunk.metadata
            }
            }
            database.append(data)
        try:
            print(f"Upsearting {len(database)} records to Vector db ...")
            if self.MAX_BATCH_SIZE > 96 :
                print(f"Batch size is Larger try again with =< 96...")
            if len(database)>1:
                for start in range(0,len(database),self.MAX_BATCH_SIZE):
                    record = database[start: start+self.MAX_BATCH_SIZE]
                    self.index.upsert(
                        namespace="qa_vec_db_sytem",
                        vectors= record
                    )
                print(f"Vectors {len(database)} Upsert sucessfully ")
        except Exception as e:
            print(f"Error {e}")