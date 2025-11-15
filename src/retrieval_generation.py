
import asyncio
import anyio.to_thread
import google.generativeai as genai 
from settings import config
import anyio


class RetrievalGenration:
    def __init__(self,vector_store: object, embedding: object,query,user_id = None):
        self.user_id = user_id
        self.vector_store = vector_store
        self.embedding = embedding
        self.query = query
        genai.configure(api_key=config.gemini_key)
        self._gemini = genai.GenerativeModel(model_name='gemini-2.5-flash')

    async def _retrieval(self):
        try:
            if not self.vector_store.index:
                raise ValueError("Vector store index is not initialized")
            
            d_e = self.embedding.get_dense_embedding(self.query)
            s_e = self.embedding.get_sparse_embedding(self.query)
            
            query_params = {
                "vector": d_e.tolist(),
                "sparse_vector": s_e,
                "top_k": 20,
                "include_metadata": True,
                "namespace": "qa_vec_db_sytem",
            }
            if self.user_id:
                query_params["filter"] = {"user_id": {"$eq": self.user_id}}

            def _retrive_query():
                return self.vector_store.index.query(**query_params)
            
            self.res = await anyio.to_thread.run_sync(_retrive_query)
            return self.res
        except Exception as e:
            print(f"Error in _retrieval: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    async def _generation(self):

        blocks = []
        for m in self.res['matches']:
            md = m.get("metadata", {}) or {}
            doc_id = m.get("id")
            uname = md.get("user_name") or "Unknown"
            uid = md.get("user_id") or "Unknown"
            ts = md.get("timestamp") or "Unknown"
            text = (md.get("text") or "").strip().replace("\r", " ")
            blocks.append(
                f"[doc:{doc_id}] user_name={uname} user_id={uid} timestamp={ts}\n{text}"
            )
        docs = "\n\n---\n\n".join(blocks) if blocks else "NO_EVIDENCE"

        GEMINI_SYSTEM_PROMPT = (
            "You are a retrieval-grounded assistant that answers user questions strictly from the provided context.\n"
            "The context may include timestamps or event details; you may consider them internally for reasoning "
            "but must never mention them explicitly.\n\n"

            "Follow these rules carefully:\n"
            "1. Use ONLY the provided context for your answer. Do not use prior knowledge.\n"
            "2. Always analyze the context before answering. If relevant details are missing, explain exactly what "
            "information is absent (for example: 'no explicit date mentioned', 'location not specified', etc.).\n"
            "3. If the question cannot be answered directly from the data, reply with:\n"
            "   'The answer cannot be determined from the available data because <reason>.'\n"
            "   (Be explicit about why — what was missing or ambiguous.)\n"
            "4. If there are partial clues, make one reasonable and clearly-labeled inference:\n"
            "   'Possible assumption: ...' (This line must follow your main answer and be logically justified.)\n"
            "5. If there is absolutely no relevant information at all, respond exactly:\n"
            "   'The answer cannot be determined from the available data because no relevant evidence was found.'\n"
            "6. Never invent or guess names, dates, or facts that do not appear in the context.\n"
             "If the name in the question differs slightly from the one represented in the context, "
            "quietly interpret it as referring to the most similar user in the data without explicitly mentioning or comparing names. "
            "Base your reasoning on that user’s information.\n" 
            "7. Keep your tone concise, factual, and natural — not robotic or verbose.\n\n"

            "Structure your output consistently as:\n"
            "Answer: <your main conclusion or 'cannot be determined' line>\n"
            "Possible assumption: <optional, only if some partial clue exists>"
        )

        Prompt= (
            f"{GEMINI_SYSTEM_PROMPT}\n\n"
            f"Question {self.query}\n\n"
            f"context: {blocks}\n\n"
            f"Answer: "
        )
        def _call():
            return self._gemini.generate_content(Prompt)
        try:
            resp = await anyio.to_thread.run_sync(_call)
            return (getattr(resp, "text", "") or "").strip()
        
        except Exception as e:
            return f"{e} Answer cannot be determine from available data"
        
    async def main(self):
        await self._retrieval()
        answer  = await self._generation()

        if not answer:
            answer = "Answer Cannot be detemined.."
        return {
            "answer" : answer
        } 


