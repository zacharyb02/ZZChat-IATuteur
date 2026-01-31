import os

def filtrer_fichiers_cnn(dossier_path):
    # Liste des mots-clés qui prouvent qu'un fichier parle de CNN
    cnn_keywords = [
        "cnn", "convolutional", "pooling", "stride", "padding", 
        "feature map", "conv2d", "backpropagation", "kernel", "filter"
    ]
    
    files_deleted = 0
    files_kept = 0

    if not os.path.exists(dossier_path):
        print(f"Erreur : Le dossier '{dossier_path}' n'existe pas.")
        return

    print(f"--- Nettoyage du dossier : {dossier_path} ---")

    for nom_fichier in os.listdir(dossier_path):
        if nom_fichier.endswith(".txt"):
            chemin_complet = os.path.join(dossier_path, nom_fichier)
            
            try:
                with open(chemin_complet, 'r', encoding='utf-8') as f:
                    contenu = f.read().lower()
                
                # Vérifier si au moins un mot-clé CNN est présent
                if any(keyword in contenu for keyword in cnn_keywords):
                    print(f"✅ GARDÉ : {nom_fichier}")
                    files_kept += 1
                else:
                    # Supprimer le fichier s'il est hors-sujet
                    print(f"❌ SUPPRIMÉ (Hors-sujet) : {nom_fichier}")
                    os.remove(chemin_complet)
                    files_deleted += 1
                    
            except Exception as e:
                print(f"⚠️ Erreur de lecture sur {nom_fichier}: {e}")

    print("\n" + "="*30)
    print(f"NETTOYAGE TERMINÉ")
    print(f"Fichiers conservés : {files_kept}")
    print(f"Fichiers supprimés : {files_deleted}")
    print("="*30)

# Remplace 'votre_dossier' par le chemin vers tes fichiers .txt
filtrer_fichiers_cnn('cnn_knowledge_base_eng')