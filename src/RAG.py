from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings # Import spécifique à Ollama
from langchain_community.vectorstores import FAISS

# 1. Charger le document
loader = PyPDFLoader("torch.nn — PyTorch 2.9 documentation.pdf")
documents = loader.load()

# 2. Découper le texte en morceaux (Chunks)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100
)
docs = text_splitter.split_documents(documents)

# 3. Choisir le modèle d'embedding d'Ollama
# Assurez-vous d'avoir fait : ollama pull mxbai-embed-large
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 4. Créer la base de données FAISS et indexer les documents
# C'est ici qu'Ollama va transformer vos textes en vecteurs numériques
vector_db = FAISS.from_documents(docs, embeddings)

# 5. Sauvegarder l'index localement
vector_db.save_local("faiss_index_pfe")

# 6. Test de recherche sémantique
query = "Quelle est la conclusion du document ?"
docs_score = vector_db.similarity_search(query)

if docs_score:
    print("Résultat de la recherche :")
    print(docs_score[0].page_content)

