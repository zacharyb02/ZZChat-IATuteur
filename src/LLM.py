import os
import time
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from codecarbon import EmissionsTracker
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
def ask_question(query):
    tracker = EmissionsTracker(save_to_file=True, output_dir=".")
    tracker.start()
    
    start_time = time.time() # Début du chrono
    # Recherche des documents pertinents (on récupère les objets 'Document' entiers)
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'fetch_k': 20})
    docs = retriever.invoke(query)
    # Préparation du contexte texte
    context_chunks = []
    #print("\n=== DOCUMENTS AND CONTEXT CHUNKS ===")
    for i, doc in enumerate(docs):
        # Découpe le texte en chunks
        text = doc.page_content
        context_chunks.append(text)
    # Combine les chunks pour le LLM
    context_for_llm = "\n\n".join(context_chunks)
# Prompt système optimisée pour un rôle de Tuteur CNN
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
            f"QUESTION DE L'ÉTUDIANT : {query}\n\n"
            "RÉPONSE DU TUTEUR :"
        ))
    ]
    print(context_for_llm)
    
    # Génération de la réponse
    response = llm.invoke(messages)

    end_time = time.time() # Fin du chrono
    emissions = tracker.stop() # Fin du suivi carbone

    inference_time = end_time - start_time
    # On retourne la réponse ET les documents sources
    return response.content , inference_time, emissions

# 5. Test avec affichage des sources
query = "What is maxpooling definition "  # Exemple de question
print(f"Question: {query}")
print("-" * 30)
answer, duration, co2 = ask_question(query)

print("\n=== METRIQUES DE PERFORMANCE ===")
print(f"⏱️ Temps d'inférence : {duration:.2f} secondes")
print(f"🌱 Émissions générées : {co2:.10f} kg CO2")
print("-" * 30)
print("\n=== TUTOR RESPONSE ===")
print(answer)