import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Configuration des Embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 2. Chargement de l'index
vector_db = FAISS.load_local(
    "faiss_index_pfe", 
    embeddings, 
    allow_dangerous_deserialization=True
)

# 3. Configuration du LLM
llm = ChatOllama(model="mistral", temperature=0,num_gpu=99,num_thread=4)

# 4. Fonction de recherche + réponse modifiée
def ask_question(query,chunk_size=500):
    # Recherche des documents pertinents (on récupère les objets 'Document' entiers)
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'fetch_k': 20})
    docs = retriever.invoke(query)
    # Préparation du contexte texte
    context_chunks = []
    #print("\n=== DOCUMENTS AND CONTEXT CHUNKS ===")
    for i, doc in enumerate(docs):
        # Affiche les métadonnées si elles existent
        metadata_info = ""
        if hasattr(doc, "metadata") and doc.metadata:
            metadata_info = " | ".join(f"{k}: {v}" for k, v in doc.metadata.items())
        #print(f"\n--- Document {i+1} --- {metadata_info}")
        
        # Découpe le texte en chunks
        text = doc.page_content
        for j in range(0, len(text), chunk_size):
            chunk = text[j:j+chunk_size].strip()
            if chunk:
                context_chunks.append(chunk)
                #print(f"\nChunk {j//chunk_size + 1}:")
                #print(chunk)
    
    # Combine les chunks pour le LLM
    context_for_llm = "\n\n".join(context_chunks)
# Prompt système optimisée pour un rôle de Tuteur CNN
    system_prompt = (
    "ROLE: You are a CNN Specialist Tutor strictly limited to the provided Knowledge Base.\n\n"
    
    "=== MANDATORY RULES (STRICT RAG) ===\n"
    "1. ZERO OUTSIDE KNOWLEDGE: You are FORBIDDEN to use any information, definitions, "
    "or code that is not explicitly present in the provided CONTEXT.\n"
    
    "2. NO HALLUCINATION: If a user asks a question that is not in the documents, "
    "you must respond: 'I am sorry, but the provided documentation does not contain "
    "information on this specific topic.'\n"
    
    "3. DIRECT EXTRACTION: Extract code and definitions exactly as they appear. "
    "Do not modify the logic or optimize the code.\n"
    
    "4. NO SITE REFERENCES: Never mention websites, URLs, or local file paths in your response.\n\n"
    
    "=== RESPONSE FORMAT ===\n"
    "Provide the answer directly and concisely. Start immediately with the technical "
    "explanation or code found in the documentation. Do not list steps, do not say 'Step 1', "
    "and do not explain your internal search process. Just give the final information."
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=(
            f"STUDY CONTEXT:\n{context_for_llm}\n\n"
            f"QUESTION DE L'ÉTUDIANT : {query}\n\n"
            "RÉPONSE DU TUTEUR :"
        ))
    ]
    
    # Génération de la réponse
    response = llm.invoke(messages)
    
    # On retourne la réponse ET les documents sources
    return response.content#,context_for_llm ,docs

# 5. Test avec affichage des sources
query = "give me definition of CNN"
print(f"Question: {query}")
print("-" * 30)
answer = ask_question(query)

print("\n=== TUTOR RESPONSE ===")
print(answer)
