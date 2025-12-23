from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# 1. Configuration des embeddings (doit être le même modèle qu'à la création)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 2. Charger l'index depuis le dossier local
# "allow_dangerous_deserialization=True" est nécessaire pour charger les fichiers .pkl de FAISS
vector_db = FAISS.load_local(
    "faiss_index_pfe", 
    embeddings, 
    allow_dangerous_deserialization=True
)

print(f"Index chargé avec succès.")

# 3. Afficher le contenu de la base de connaissance
# Accès au dictionnaire interne de FAISS via LangChain
all_docs = vector_db.docstore._dict

print(f"Nombre total de morceaux (chunks) dans l'index : {len(all_docs)}")
print("-" * 50)

# Boucle pour afficher chaque morceau de texte
for doc_id, doc in all_docs.items():
    print(f"\n[ID: {doc_id}]")
    print(f"Source: {doc.metadata.get('source', 'Inconnue')}")
    print(f"Contenu (extrait) : {doc.page_content[:300]}...") # Affiche les 300 premiers caractères
    print("-" * 30)