from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings # Import spécifique à Ollama
from langchain_community.vectorstores import FAISS
import os
from langchain_community.document_loaders import TextLoader
from pathlib import Path

# 1. Charger le document
knowledge_base = Path(r"C:\Users\mohaa\Desktop\IA\AI-Tutor\cnn_knowledge_base_en")
nom_index_faiss = "faiss_index_pfe"
modele_ollama = "mxbai-embed-large"

# 1. Récupérer la liste des fichiers
files = list(knowledge_base.glob("**/*.txt"))

print(f"{len(files)} fichiers trouvés dans {knowledge_base}...")

tous_les_documents = []

# --- BOUCLE DE CHARGEMENT ---
for file_path in files:
    try:
        # On charge le fichier individuellement
        loader = TextLoader(str(file_path), encoding="utf-8") 
        documents = loader.load()
        
        # IMPORTANT : On AJOUTE à la liste globale au lieu d'écraser
        tous_les_documents.extend(documents)
        print(f"  Chargé : {file_path.name}")
        
    except Exception as e:
        print(f" Erreur sur {file_path.name} : {e}")

# --- TRAITEMENT GLOBAL (Une fois que tout est chargé) ---

if tous_les_documents:
    print(f"\nTraitement de {len(tous_les_documents)} documents chargés...")

    # 2. Découper le texte en morceaux (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900, 
        chunk_overlap=90
    )
    
    # On découpe TOUT d'un coup
    docs = text_splitter.split_documents(tous_les_documents)
    print(f"Génération de {len(docs)} chunks...")

    # 3. Choisir le modèle d'embedding d'Ollama
    embeddings = OllamaEmbeddings(model=modele_ollama)

    # 4. Créer la base de données FAISS et indexer les documents
    print("Vectorisation et indexation en cours (patience)...")
    vector_db = FAISS.from_documents(docs, embeddings)

    # 5. Sauvegarder l'index localement
    vector_db.save_local(nom_index_faiss)
    print(f"Index sauvegardé avec succès dans le dossier '{nom_index_faiss}'")

    # 6. Test de recherche sémantique
    query = "Quelle est la conclusion du document ?"
    docs_score = vector_db.similarity_search(query)

    if docs_score:
        print("\n--- Test de Résultat ---")
        # On affiche la source pour vérifier que ça marche bien
        source = docs_score[0].metadata.get('source', 'Inconnu')
        print(f"Source : {source}")
        print(docs_score[0].page_content)
    else:
        print("Aucun résultat trouvé.")

else:
    print("Aucun document n'a été chargé correctement.")