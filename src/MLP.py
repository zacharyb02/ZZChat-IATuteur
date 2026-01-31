import os
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import classification_report
from codecarbon import EmissionsTracker

# Désactivation des messages TensorFlow inutiles
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 1. Tracking énergétique
tracker = EmissionsTracker(project_name="MLP_Augmented")
tracker.start()

# 2. Chargement des données
# On active shuffle=True pour l'entraînement
train_ds = tf.keras.utils.image_dataset_from_directory(
    'banana_sushi/train',
    image_size=(128, 128),
    batch_size=32,
    label_mode='categorical',
    shuffle=True  # TRÈS IMPORTANT ici
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    'banana_sushi/val',
    image_size=(128, 128),
    batch_size=32,
    label_mode='categorical',
    shuffle=False # Pas besoin pour l'évaluation
)

# 3. Définition de la couche de Data Augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),     # Retourne l'image horizontalement
    layers.RandomRotation(0.1),          # Rotation aléatoire de 10%
    layers.RandomZoom(0.1),              # Zoom aléatoire
])

# 4. Construction du Modèle MLP avec Augmentation
model = models.Sequential([
    # Entrée et Augmentation
    layers.Input(shape=(128, 128, 3)),
    data_augmentation,
    
    # Prétraitement
    layers.Rescaling(1./255),
    
    # Architecture MLP
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.3),                 # Dropout pour éviter le surapprentissage
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(4, activation='softmax')
])

model.compile(
    optimizer='adam', 
    loss='categorical_crossentropy', 
    metrics=['accuracy']
)

# 5. Entraînement
print("Lancement de l'entraînement MLP avec Data Augmentation...")
model.fit(train_ds, validation_data=val_ds, epochs=15)

# 6. Évaluation
print("\n--- RÉSULTATS MLP AUGMENTÉ ---")
y_true = []
y_pred = []
for images, labels in val_ds:
    y_true.extend(tf.argmax(labels, axis=1).numpy())
    y_pred.extend(tf.argmax(model.predict(images, verbose=0), axis=1).numpy())

print(classification_report(y_true, y_pred, target_names=['Classe 1', 'Classe 2', 'Classe 3', 'Classe 4']))

tracker.stop()