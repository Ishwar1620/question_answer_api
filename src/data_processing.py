from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
from settings import config
import numpy as np
import requests
import os
load_dotenv()

class DataProcessing:
    def __init__(self):
        self.data_embedding_model = HuggingFaceBgeEmbeddings(model_name='all-MiniLM-L6-V2')
        self.data_url = config.public_data_url
        self.param = config.data_api_param
        self.process_data = []

    def _message_formating(self,data):
        user_id = data['user_id']
        time_stamp = data['timestamp']
        User_name = data['user_name']
        message = data['message']

        return f"User:{User_name}\nmessage:{message}".strip()

    def chunked_prerocess(self):
        temp_docs = []
        try:
            response = requests.get(self.data_url,self.param)
            data = response.json()
            user_name = [data['items'][i]['user_name'] for i in range(len(data['items']))]
            user_name= np.unique(np.array(user_name)).tolist()
            user_id = [data['items'][i]['user_id'] for i in range(len(data['items']))]
            user_id= np.unique(np.array(user_id)).tolist()

            for un,uid in zip(user_name,user_id):
                temp = [item for item in data['items'] if item['user_name'] == un]
                temp_message = [f"{i['timestamp']} | {i['message']}" for i in temp]
                temp_message = '\n'.join(temp_message)
                dict = {
                    'user_id':uid,
                    'user_name':un,
                    'message':temp_message
                }
                doc = Document(
                    page_content=dict['message'],
                    metadata = {
                        'user_id' : dict['user_id'],
                        'user_name' :dict['user_name']
                    }
                )
                temp_docs.append(doc)

            semantic_splitter = SemanticChunker(
            embeddings= self.data_embedding_model,
            breakpoint_threshold_type='percentile',
            breakpoint_threshold_amount=0.4,
            min_chunk_size= 800,)

            self.process_data=semantic_splitter.split_documents(temp_docs)
            
            return self.process_data
        except Exception as e :
            print(f"Error {e}")
    def preprocess(self):
        try:
            response = requests.get(self.data_url,self.param)
            data = response.json()
            for i, item in enumerate(data['items']):
                message = self._message_formating(item)
                doc= Document(
                    page_content= message,#item['message'],
                    metadata = {
                        'id': item['id'],
                        'timestamp': item['timestamp'],
                        'user_id': item['user_id'],
                        'user_name': item['user_name']
                    }
                )
                self.process_data.append(doc)
            return self.process_data
        except Exception as e :
            print(f"Error {e}")

