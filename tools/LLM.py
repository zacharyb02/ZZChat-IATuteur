import os

import time
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from codecarbon import EmissionsTracker

# =========================
# 1. Embeddings
# =========================
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# =========================
# 2. Load FAISS index
# =========================
# vector_db = FAISS.load_local(
#     "faiss_index_pfe",
#     embeddings,
#     allow_dangerous_deserialization=True
# )
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to FAISS index
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index_pfe")

vector_db = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# =========================
# 3. LLM configuration
# =========================
llm = ChatOllama(
    model="mistral",
    temperature=0,
    num_gpu=99,
    num_thread=4
)

# =========================
# 4. MAIN FUNCTION USED BY BACKEND
# =========================
def ask_question(query: str):
    """
    Takes a user query (text only),
    performs RAG over FAISS,
    returns:
      - answer (str)
      - inference_time (float)
      - emissions (float)
    """

    tracker = EmissionsTracker(save_to_file=True, output_dir=".")
    tracker.start()
    start_time = time.time()

    # ---- Retrieve documents
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 20}
    )
    docs = retriever.invoke(query)

    # ---- Build context
    context_chunks = [doc.page_content for doc in docs]
    context_for_llm = "\n\n".join(context_chunks)

    # ---- System prompt (STRICT RAG)
    system_prompt = (
    "ROLE: CNN Specialist Assistant - STRICT DATA RETRIEVAL ONLY.\n\n"
    
    "=== THE GOLDEN RULE ===\n"
    "You are an AI assistant specialized ONLY in Convolutional Neural Networks (CNN). "
    "Your knowledge is strictly limited to the provided documentation (RAG).\n\n"
    
    "=== STRICT BEHAVIORAL PROTOCOL ===\n"
    "If the answer is not explicitly found within the provided context, or if the question is outside the scope of Convolutional Neural Networks (CNN), you must respond EXACTLY and ONLY with: 'I don't know.' Do not provide any other text."
    
    "2. 100% GROUNDING: Do not use your own training data. You are forbidden from "
    "generating information that is not explicitly present in the provided context. "
    "If the answer is missing from the context: 'I don't know.'\n"
    
    "3. 100% CONTEXT: You must answer based ONLY on the documentation. Do not add outside "
    "definitions of Quantum Computing. If the answer is not a CNN technical detail found in the text, "
    "the response is: 'I don't know.'\n"
    
    "4. NO FORMATTING/PREAMBLE: Do not use greetings (Hello, Hi). Start the answer "
    "directly with the relevant technical content or the refusal string.\n\n"
    
    "=== VERIFICATION ===\n"
    "Question is CNN + In Context -> Direct answer.\n"
    "Question is NOT CNN OR Not In Context -> I don't know."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=(
            f"STUDY CONTEXT:\n{context_for_llm}\n\n"
            f"STUDENT QUESTION:\n{query}\n\n"
            "ANSWER:"
        ))
    ]

    # ---- LLM call
    response = llm.invoke(messages)

    end_time = time.time()
    emissions = tracker.stop()

    inference_time = end_time - start_time

    return response.content.strip(), inference_time, emissions

