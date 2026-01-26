import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# --- CONFIGURATION ---
OUTPUT_FOLDER = "knowledge_base_cnn"
MAX_DEPTH = 2           # Réduit à 2 pour éviter de trop s'éloigner du sujet
MAX_PAGES = 30          # Par site
TIMEOUT = 10

# Headers pour ne pas se faire bloquer
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Mots-clés pour valider qu'une page est pertinente
KEYWORDS_CNN = [
    "cnn", "convolution", "pooling", "stride", "padding", "relu", 
    "softmax", "adam", "sgd", "pytorch", "tensorflow", "keras", 
    "layer", "model", "training", "loss", "accuracy", "codecarbon", 
    "emission", "tracker", "inference", "neural"
]

visited_urls = set()
pages_saved_count = 0

def nettoyer_nom_fichier(url):
    """Crée un nom de fichier propre à partir de l'URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    if not path: path = "home"
    domain = parsed.netloc.replace("www.", "").replace(".", "_")
    filename = f"{domain}_{path}"
    # Garde seulement les caractères alphanumériques et underscores
    clean_name = "".join([c for c in filename if c.isalnum() or c == '_'])
    return clean_name[:100] + ".txt"

def extraire_contenu_intelligent(soup):
    """
    Extrait le texte et le CODE en respectant la structure.
    CORRECTION MAJEURE : Préservation de l'indentation et des lignes de code.
    """
    # 1. Nettoyage des balises inutiles
    for balise in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg", "button", "iframe", "ad"]):
        balise.decompose()

    # 2. Trouver le contenu principal
    corps = soup.find('main') or soup.find('article') or soup.find('div', {'role': 'main'}) or soup.find('div', class_='content') or soup.body
    
    if not corps:
        return ""

    contenu_final = []
    textes_vus = set()

    # 3. Parcours intelligent des éléments
    # On ajoute 'code' et les classes spécifiques aux docs techniques
    tags_to_find = ['h1', 'h2', 'h3', 'p', 'pre', 'code', 'div', 'li']
    
    all_elements = corps.find_all(tags_to_find)

    for element in all_elements:
        text_content = ""
        is_code = False
        prefix = ""

        # --- CAS 1 : CODE PYTHON ---
        classes = element.get('class', [])
        
        # Détection améliorée pour TensorFlow, PyTorch, GitHub, etc.
        is_pre_block = element.name == 'pre'
        is_code_div = element.name == 'div' and ('highlight' in classes or 'code' in classes or 'devsite-code-button' in str(classes))
        
        # On ignore les balises 'code' qui sont à l'intérieur d'un 'pre' (pour éviter les doublons)
        if element.name == 'code' and element.find_parent('pre'):
            continue

        if is_pre_block or is_code_div:
            is_code = True
            # --- CORRECTION ICI ---
            # On N'UTILISE PAS separator="\n" pour le code, sinon ça casse tout.
            # On utilise get_text() brut pour garder les espaces et indentations.
            text_content = element.get_text().strip()
        
        # --- CAS 2 : TITRES ---
        elif element.name in ['h1', 'h2', 'h3']:
            text_content = element.get_text(strip=True)
            prefix = "\n\n" + "#" * int(element.name[1]) + " "
        
        # --- CAS 3 : TEXTE NORMAL ---
        elif element.name in ['p', 'li']:
            # On ignore les paragraphes qui sont DANS un tableau ou du code
            if element.find_parent(['table', 'pre', 'div'], class_='highlight'):
                continue
            
            # Pour le texte, on veut des espaces entre les balises inline (comme les liens)
            text_content = element.get_text(" ", strip=True)
            if element.name == 'li':
                prefix = "- "

        # --- FILTRAGE ET AJOUT ---
        if text_content and text_content not in textes_vus:
            
            if is_code:
                # Nettoyage spécifique code : on retire les lignes vides multiples
                lines = [line for line in text_content.splitlines() if line.strip()]
                cleaned_code = "\n".join(lines)
                
                # On ne garde que les blocs de code > 20 caractères
                if len(cleaned_code) > 20:
                    # On vérifie que ce n'est pas juste des commandes shell inutiles
                    if "pip install" in cleaned_code and len(cleaned_code) < 50:
                        continue

                    block = f"\n\n```python\n{cleaned_code}\n```\n\n"
                    contenu_final.append(block)
                    textes_vus.add(text_content) # On ajoute le brut au set pour éviter doublons
            
            else:
                # Pour le texte normal
                if len(text_content) > 30 or element.name.startswith('h'):
                    contenu_final.append(f"{prefix}{text_content}")
                    textes_vus.add(text_content)

    return "\n".join(contenu_final)

def crawler(url, current_depth, domain_restriction):
    global pages_saved_count
    
    if current_depth > MAX_DEPTH or url in visited_urls:
        return

    visited_urls.add(url)
    print(f"[{current_depth}] Scan: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code != 200: return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraction
        texte_propre = extraire_contenu_intelligent(soup)

        # SAUVEGARDE (Uniquement si contenu suffisant)
        if len(texte_propre) > 500:
            filename = nettoyer_nom_fichier(url)
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                # ⚠️ IMPORTANT : PLUS DE "SUJET:" NI DE METADATA EN HAUT
                # On met juste l'URL en commentaire tout en bas si besoin
                f.write(texte_propre)
                f.write(f"\n\n# Source: {url}")
            
            print(f"   -> Sauvegardé : {filename} ({len(texte_propre)} chars)")
            pages_saved_count += 1
        else:
            print("   -> Ignoré (Contenu trop court/vide)")

        # NAVIGATION (Récursive)
        if current_depth < MAX_DEPTH:
            for lien in soup.find_all('a', href=True):
                full_url = urljoin(url, lien['href']).split('#')[0]
                
                # On reste sur le même domaine et on évite les doublons
                if domain_restriction in full_url and full_url not in visited_urls:
                    # Filtre simple sur les mots clés dans l'URL pour rester pertinent
                    if any(kw in full_url.lower() for kw in KEYWORDS_CNN) or "tutorial" in full_url:
                        crawler(full_url, current_depth + 1, domain_restriction)

    except Exception as e:
        print(f"   -> Erreur: {e}")

# --- LANCEMENT ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    # Liste ciblée (Docs officielles + Tutoriels fiables)
    urls_cibles = [
        # --- 1. LES INDISPENSABLES (DOCS OFFICIELLES) ---
    # Ces pages sont "propres" et contiennent le code exact que l'IA doit apprendre.
    
    # TensorFlow / Keras (Le standard pour débuter)
    "https://www.tensorflow.org/tutorials/images/cnn",
    "https://www.tensorflow.org/tutorials/images/classification",
    "https://www.tensorflow.org/tutorials/images/data_augmentation",
    "https://www.tensorflow.org/tutorials/images/transfer_learning",
    "https://www.tensorflow.org/guide/keras/functional",  # Pour les architectures complexes

    # PyTorch (Le standard recherche/industrie)
    "https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html",
    "https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html",
    "https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html",
    "https://pytorch.org/tutorials/recipes/recipes/defining_a_neural_network.html",

    # --- 2. THÉORIE APPROFONDIE (BIBLE DES CNN) ---
    # Stanford CS231n : C'est la référence mondiale. Très riche en texte explicatif.
    "https://cs231n.github.io/convolutional-networks/",
    "https://cs231n.github.io/neural-networks-1/",
    "https://cs231n.github.io/neural-networks-2/",
    "https://cs231n.github.io/optimization-1/",
    
    # MIT Deep Learning
    "http://introtodeeplearning.com/", 

    # --- 3. TUTORIELS PRATIQUES & CODE ---
    # Machine Learning Mastery (Très facile à scraper, format clair)
    "https://machinelearningmastery.com/convolutional-layers-for-deep-learning-neural-networks/",
    "https://machinelearningmastery.com/how-to-develop-a-cnn-from-scratch-for-cifar-10-photo-classification/",
    "https://machinelearningmastery.com/image-augmentation-deep-learning-keras/",
    
    # Papers with Code (Pour relier théorie et implémentation)
    "https://paperswithcode.com/method/cnn",
    "https://paperswithcode.com/method/resnet",
    
    # --- 4. GREEN AI & MLOps (Ton exigence spécifique) ---
    # CodeCarbon & Mesure d'énergie
    "https://mlco2.github.io/codecarbon/usage.html",
    "https://mlco2.github.io/codecarbon/methodology.html",
    "https://mlco2.github.io/codecarbon/parameters.html",
    
    # Hugging Face (Documentation efficace)
    "https://huggingface.co/docs/transformers/tasks/image_classification",

    # --- 5. MATHÉMATIQUES & CONCEPTS CLÉS ---
    # Explications visuelles des convolutions
    "https://poloclub.github.io/cnn-explainer/",  # Attention: bcp de visuel, peut-être dur à scraper
    "https://distill.pub/2017/feature-visualization/", # Excellent mais complexe techniquement
    
    # --- 6. ARCHITECTURES CÉLÈBRES ---
    "https://iq.opengenus.org/vgg16/",
    "https://iq.opengenus.org/resnet50-architecture/",
    "https://iq.opengenus.org/mobile-net-architecture/"
    ]

    print("--- Démarrage du Scraping Optimisé ---")
    
    for url in urls_cibles:
        domain = urlparse(url).netloc
        crawler(url, 0, domain)
    
    print(f"\nTerminé ! {pages_saved_count} pages extraites avec succès.")