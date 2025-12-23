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
llm = ChatOllama(model="deepseek-coder", temperature=0)

# 4. Fonction de recherche + réponse modifiée
def ask_question(query):
    # Recherche des documents pertinents (on récupère les objets 'Document' entiers)
    docs = vector_db.similarity_search(query, k=3)
    
    # Préparation du contexte pour l'IA
    context = "\n".join([d.page_content for d in docs])
    print('==CONTEXT==')
    print(context)
    print('==========')
    # Structure de messages
    messages = [
        SystemMessage(content=(
            "Tu es un assistant expert en analyse de documents. "
            "Réponds en français en te basant sur le CONTEXTE fourni."
        )),
        HumanMessage(content=(
            f"CONTEXTE :\n{context}\n\n"
            f"QUESTION : {query}\n\n"
            "RÉPONSE :"
        ))
    ]
    
    # Génération de la réponse
    response = llm.invoke(messages)
    
    # On retourne la réponse ET les documents sources
    return response.content

# 5. Test avec affichage des sources
query = "c quoi nn.Conv1d"
print(f"Question: {query}")
print("-" * 30)

answer = ask_question(query)

print("RÉPONSE DE DEEPSEEK :")
print(answer)
print("\n" + "="*50)
print("EXTRAITS DU DOCUMENT UTILISÉS (SOURCES) :")
print("="*50)
