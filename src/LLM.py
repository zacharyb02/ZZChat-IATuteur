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
    print("\n=== DOCUMENTS AND CONTEXT CHUNKS ===")
    for i, doc in enumerate(docs):
        # Affiche les métadonnées si elles existent
        metadata_info = ""
        if hasattr(doc, "metadata") and doc.metadata:
            metadata_info = " | ".join(f"{k}: {v}" for k, v in doc.metadata.items())
        print(f"\n--- Document {i+1} --- {metadata_info}")
        
        # Découpe le texte en chunks
        text = doc.page_content
        for j in range(0, len(text), chunk_size):
            chunk = text[j:j+chunk_size].strip()
            if chunk:
                context_chunks.append(chunk)
                print(f"\nChunk {j//chunk_size + 1}:")
                print(chunk)
    
    # Combine les chunks pour le LLM
    context_for_llm = "\n\n".join(context_chunks)
# Prompt système optimisée pour un rôle de Tuteur CNN
    system_prompt = (
       "You are an AI Tutor specialized in Deep Learning, with strong expertise in Convolutional Neural Networks (CNNs).\n"
        "Your mission is to help the student understand theoretical concepts, design robust CNN architectures, "
        "and debug Deep Learning code in a clear and pedagogical way.\n\n"
        "==================================================\n"
        "INSTRUCTIONS (MUST BE STRICTLY FOLLOWED)\n"
        "==================================================\n"
        "1. SOURCE PRIORITY: Primarily rely on the provided CONTEXT. Quote or accurately rephrase it if the answer exists there.\n"
        "2. PEDAGOGY & EXPLANATION: Always explain 'why' and 'how'. For code or model mistakes, explain the cause and consequences.\n"
        "3. CODE QUALITY: If providing code (Python, PyTorch, TensorFlow, Keras), make it clean, optimized, and commented line by line for beginners.\n"
        "4. HONESTY: If the answer is NOT in the context, explicitly state so, then provide general knowledge as complementary information.\n"
        "5. LANGUAGE & STYLE: Always respond in clear, professional, well-structured English.\n"
        "=================================================="
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
    return response.content,context_for_llm ,docs

# 5. Test avec affichage des sources
query = "give me definition of CNN"
print(f"Question: {query}")
print("-" * 30)
answer, context_chunks, source_docs = ask_question(query)

print("\n=== TUTOR RESPONSE ===")
print(answer)
"""print("\n" + "="*50)
print("SOURCE DOCUMENTS METADATA :")
print("="*50)
for i, doc in enumerate(source_docs):
    print(f"\n--- Document {i+1} ---")
    if hasattr(doc, "metadata") and doc.metadata:
        for k, v in doc.metadata.items():
            print(f"{k}: {v}")

print("\n" + "="*50)
print("TEXT CHUNKS USED AS CONTEXT :")
print("="*50)
for i, chunk in enumerate(context_chunks):
    print(f"\n--- Chunk {i+1} ---")
    print(chunk) # Affiche le texte complet du chunk
    print("-" * 20)"""