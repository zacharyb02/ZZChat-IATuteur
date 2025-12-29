import os
import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# --- CONFIGURATION ---
OUTPUT_FOLDER = "knowledge_base_cnn"
MAX_DEPTH = 3     
MAX_PAGES = 50    
DELAY = 0.5

# --- MOTS-CLÉS CIBLES ---
KEYWORDS_CNN = [
    "cnn", "conv", "convolution", "pooling", "stride", "padding","Supervised Learning","Unsupervised Learning","Training","Convolution","ReLU","Sigmoid","Hinge Loss","Focal Loss"
    "image", "vision", "feature_map", "kernel", "filter","Tanh","Softmax","Adaptive Pooling","Dense Layer","Classification Layer","Stochastic Gradient Descent (SGD)","Adam","Learning Rate","Optimizer"
    "resnet", "vgg", "alexnet", "inception", "mobilenet","Global Average Pooling","Global Max Pooling","Output Layer","Batch Normalization","Gradient Descent","Image Classification",
    "classification", "detection" ,"Layer Normalization","Instance Normalization","Dropout","Weight Decay","L1 Regularization","L2 Regularization","Loss","Binary Cross-Entropy","Categorical Cross-Entropy","Sparse Categorical Cross-Entropy","Mean Squared Error (MSE)","Mean Absolute Error (MAE)"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

visited_urls = set()
pages_scanned = 0
pages_saved = 0

def nettoyer_nom_fichier(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    if not path: path = "index"
    domain = parsed.netloc.replace("www.", "").replace(".", "_")
    filename = f"{domain}_{path}"
    
    return "".join([c for c in filename if c.isalnum() or c in ('_')]).strip()[:100] + ".txt"


def nettoyer_texte_final(texte):
    """
    Nettoie le texte brut pour le rendre lisible ligne par ligne.
    """
    lines = []
    for line in texte.splitlines():
        cleaned = line.strip()
        # On garde la ligne si elle n'est pas vide
        if cleaned:
            lines.append(cleaned)
    
    # On rejoint tout
    result = "\n".join(lines)
    
    # On supprime les accumulations de sauts de ligne (max 2)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


def extraire_contenu(soup):
    # 1. On vire tout ce qui pollue la lecture
    for balise in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg", "button", "input"]):
        balise.decompose()

    # On cible le contenu principal
    corps = soup.find('main') or soup.find('article') or soup.find('div', {'role': 'main'}) or soup.body
    if not corps: return ""

    contenu = []
    
    # Ordre de scan
    tags = ['h1', 'h2', 'h3', 'p', 'pre', 'li', 'div'] 
    
    # On utilise un Set pour éviter de scanner deux fois le même texte (fréquent avec les div imbriquées)
    textes_vus = set()

    for element in corps.find_all(tags):
        
        # --- GESTION DU CODE (C'est là que ça change) ---
        if element.name == 'pre':
            # IMPORTANT : On ne met PAS de separator="\n" ici pour le code
            # On récupère le texte brut tel qu'il est affiché
            code_text = element.get_text().strip()
            
            # On évite les doublons et les blocs vides
            if code_text and code_text not in textes_vus:
                contenu.append(f"\n```python\n{code_text}\n```\n")
                textes_vus.add(code_text)
        
        # --- GESTION DES TITRES ---
        elif element.name in ['h1', 'h2', 'h3']:
            text = element.get_text(strip=True)
            if text and text not in textes_vus:
                contenu.append(f"\n\n{'#' * int(element.name[1])} {text}\n")
                textes_vus.add(text)

        # --- GESTION DU TEXTE STANDARD ---
        elif element.name in ['p', 'li']:
            # On ignore si c'est dans un bloc de code ou un tableau
            if element.find_parent(['pre', 'table']):
                continue
                
            text = element.get_text(" ", strip=True) # On remplace les sauts internes par des espaces
            
            # Filtre : on ne garde que les phrases qui ont du sens (plus de 20 caractères ou commence par une majuscule)
            if len(text) > 20 or (text and text[0].isupper()):
                if text not in textes_vus:
                    prefix = "- " if element.name == 'li' else ""
                    contenu.append(f"{prefix}{text}")
                    textes_vus.add(text)

    # On assemble et on passe le grand nettoyage final
    texte_brut = "\n".join(contenu)
    return nettoyer_texte_final(texte_brut)

def lien_est_interessant(lien_element, url_complete):
    """
    Vérifie si un lien vaut la peine d'être cliqué.
    On regarde : 
    1. Le texte du lien (ex: "Comprendre les Convolutions")
    2. L'URL elle-même (ex: .../tf/keras/layers/Conv2D)
    """
    texte_lien = lien_element.get_text(strip=True).lower()
    url_lower = url_complete.lower()
    
    # Si un mot clé est dans le TEXTE du lien OU dans l'URL
    match_texte = any(k in texte_lien for k in KEYWORDS_CNN)
    match_url = any(k in url_lower for k in KEYWORDS_CNN)
    
    return match_texte or match_url

def crawler(url, current_depth, domain_restriction):
    global pages_scanned, pages_saved
    
    if current_depth > MAX_DEPTH or pages_scanned >= MAX_PAGES or url in visited_urls:
        return

    visited_urls.add(url)
    pages_scanned += 1
    
    print(f" Scan (Prof {current_depth}): {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200: 
            print(f"   -> Erreur Status: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraction du texte
        texte = extraire_contenu(soup)
        
        # On sauvegarde si le texte est long OU si c'est la page de départ (depth 0)
        # On s'assure juste qu'il y a un minimum de contenu (> 50 chars) pour éviter les pages blanches
        if len(texte) > 500 or (current_depth == 0 and len(texte) > 50):
            filename = nettoyer_nom_fichier(url)
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"SOURCE_URL: {url}\nSUJET: CNN_DEEP_LEARNING\n\n{texte}")
            
            print(f"    [V] Sauvegardé ({len(texte)} chars)")
            pages_saved += 1
        else:
            print(f"    [X] Ignoré (Contenu trop court: {len(texte)} chars)")

        # 2. NAVIGATION FILTRÉE
        if current_depth < MAX_DEPTH:
            liens = soup.find_all('a', href=True)
            for lien in liens:
                full_url = urljoin(url, lien['href']).split('#')[0]
                
                # Vérification du domaine
                if urlparse(full_url).netloc == domain_restriction:
                    if full_url not in visited_urls:
                        # Si le lien est intéressant OU si on est sur la page d'accueil (pour trouver le sommaire)
                        if lien_est_interessant(lien, full_url) or (current_depth == 0 and "tutorial" in full_url):
                            crawler(full_url, current_depth + 1, domain_restriction)

    except Exception as e:
        print(f" Erreur critique : {e}")


# --- LANCEMENT ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # --- LISTE STRATÉGIQUE POUR LE PROJET RAG ---
    start_urls_list = [
        # 1. MLP (Perceptron Multicouche) - Scikit-Learn
        "https://scikit-learn.org/stable/modules/neural_networks_supervised.html",
        
        # 2. CNN (Réseaux Convolutifs) - TensorFlow
        "https://www.tensorflow.org/tutorials/images/cnn",
        "https://www.tensorflow.org/tutorials/images/classification",
        
        # 3. Transfer Learning - TensorFlow
        "https://www.tensorflow.org/tutorials/images/transfer_learning",
        
        # 4. PyTorch (CNN & Transfer Learning) - Alternative demandée
        "https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html",
        "https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html",
        #datacamp
        "https://www.datacamp.com/tutorial/introduction-to-convolutional-neural-networks-cnns?utm_source=chatgpt.com",
        "https://learnopencv.com/understanding-convolutional-neural-networks-cnn/?utm_source=chatgpt.com",
        "https://cs231n.github.io/convolutional-networks/?utm_source=chatgpt.com",
        "https://training.galaxyproject.org/training-material/topics/statistics/tutorials/CNN/tutorial.html?utm_source=chatgpt.com",
        "https://www.projectpro.io/article/learn-convolutional-neural-networks/803?utm_source=chatgpt.com",
        "https://www.scribd.com/document/892468764/cours-CNN-1?utm_source=chatgpt.com",
        "https://www.geeksforgeeks.org/deep-learning/building-a-convolutional-neural-network-using-pytorch/?utm_source=chatgpt.com",
        "https://www.kaggle.com/code/kanncaa1/convolutional-neural-network-cnn-tutorial?utm_source=chatgpt.com",
        ""
        # 5. Green AI & CodeCarbon (Dimension Énergétique - OBLIGATOIRE)
        "https://mlco2.github.io/codecarbon/usage.html",
        "https://mlco2.github.io/codecarbon/methodology.html",
        "https://deeplearning.stanford.edu/tutorial/supervised/ConvolutionalNeuralNetwork/",
        "https://www.datacamp.com/tutorial/introduction-to-convolutional-neural-networks-cnns",
        "https://learnopencv.com/understanding-convolutional-neural-networks-cnn/",
        "https://training.galaxyproject.org/training-material/topics/statistics/tutorials/CNN/tutorial.html",
        "https://www.coursera.org/learn/convolutional-neural-networks",
        "https://www.tensorflow.org/tutorials/images/cnn",
        "https://poloclub.github.io/cnn-explainer/",
        "https://medium.com/@prathammodi001/convolutional-neural-networks-for-dummies-a-step-by-step-cnn-tutorial-e68f464d608f",
        "https://d2l.ai/chapter_convolutional-neural-networks/",
        "https://cs231n.github.io/convolutional-networks/",
        "https://parktwin2.medium.com/building-a-convolutional-neural-network-cnn-with-pytorch-bdd3c5fe47cb"

    ]

    # --- DANS LA SECTION IF NAME == MAIN ---

    print("--- Démarrage du Scraping Multi-Sources ---")
    
    # Boucle sur chaque URL de la liste
    for i, url in enumerate(start_urls_list):
        if not url.strip(): continue # Saute les lignes vides

        print(f"\n [Source {i+1}/{len(start_urls_list)}] Traitement de : {url}")
        
        domain_start = urlparse(url).netloc
    
        # On remet le compteur à zéro pour chaque nouveau site
        # Sinon le premier site mange tout le budget de pages !
        pages_scanned = 0 
        
        # Optionnel : On remet visited_urls à zéro si on veut traiter 
        # des pages similaires sur des sites différents, 
        # mais garder le set évite les boucles infinies.
        # visited_urls.clear() 

        crawler(url, 0, domain_start)

    print(f"\n GRAND TOTAL : {pages_saved} pages sauvegardées.")