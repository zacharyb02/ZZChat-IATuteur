import os

# Ton dossier
folder_path = r"C:\Users\mohaa\Desktop\IA\AI-Tutor\knowledge_base_cnn"

print(f"Nettoyage des fichiers dans : {folder_path}")

count = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        try:
            # 1. Lire le fichier
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # 2. Garder seulement les lignes qui ne sont PAS des métadonnées
            new_lines = []
            for line in lines:
                # On met la ligne en minuscules juste pour la vérification (.lower())
                line_lower = line.strip().lower()
                
                # Si la ligne ne commence pas par un de ces mots-clés, on la garde
                if not line_lower.startswith("source_url:") \
                   and not line_lower.startswith("sujet:") \
                   and not line_lower.startswith("source:"):
                    new_lines.append(line)
            
            # 3. Réécrire le fichier propre
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
                
            print(f"✅ Nettoyé : {filename}")
            count += 1
            
        except Exception as e:
            print(f"❌ Erreur sur {filename} : {e}")

print(f"\nTerminé ! {count} fichiers ont été nettoyés.")