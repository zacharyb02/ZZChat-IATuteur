import os
from PIL import Image

def resize_images(root_path, size=(128, 128)):
    """
    Parcourt les dossiers de classes et redimensionne toutes les images.
    """
    # Formats d'images acceptés
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    
    print(f"Début du redimensionnement dans : {root_path}")
    
    for subdir, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(subdir, file)
                
                try:
                    with Image.open(file_path) as img:
                        # Conversion en RGB (pour éviter les erreurs avec les PNG en RGBA)
                        img = img.convert('RGB')
                        # Redimensionnement
                        img_resized = img.resize(size, Image.Resampling.LANCZOS)
                        # Sauvegarde (écrase l'original pour gagner de la place)
                        img_resized.save(file_path)
                except Exception as e:
                    print(f"Erreur sur {file_path} : {e}")

# Utilisation pour vos deux dossiers
path_train = 'banana_sushi/train'
path_val = 'banana_sushi/val'

resize_images(path_train)
resize_images(path_val)

print("Opération terminée avec succès !")