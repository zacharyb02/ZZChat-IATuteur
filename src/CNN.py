import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from codecarbon import EmissionsTracker
from sklearn.metrics import classification_report


# 1. Suivi énergétique avec CodeCarbon
tracker = EmissionsTracker(project_name="Transfer_Learning_Final")
tracker.start()

# 1. Charger les données (Assurez-vous d'avoir bien fait le resize 128x128 avant)
train_ds = tf.keras.utils.image_dataset_from_directory(
    'banana_sushi/train', image_size=(128, 128), batch_size=16, label_mode='categorical'
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    'banana_sushi/val', image_size=(128, 128), batch_size=16, label_mode='categorical', shuffle=False
)

# 2. Base pré-entraînée
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3), include_top=False, weights='imagenet'
)
base_model.trainable = False 

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.2),
])

# 3. Modèle complet
model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),
    data_augmentation,
    layers.Lambda(tf.keras.applications.mobilenet_v2.preprocess_input),
    base_model,
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4), # Augmenté pour éviter le surapprentissage sur 72 images
    layers.Dense(4, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement rapide de la tête
model.fit(train_ds, validation_data=val_ds, epochs=15)
model.save('model_CNN.h5')
# 7. Fin du suivi énergétique
emissions = tracker.stop()
print("\n" + "="*30)
print("RÉSULTATS D'ÉVALUATION")
print("="*30)

y_true = []
y_pred = []

# Extraction des prédictions sur le jeu de validation
for images, labels in val_ds:
    preds = model.predict(images, verbose=0)
    y_true.extend(np.argmax(labels, axis=1))
    y_pred.extend(np.argmax(preds, axis=1))

# Affichage du rapport complet (F1-score inclus)
target_names = train_ds.class_names
print(classification_report(y_true, y_pred, target_names=target_names))

print(f"\n[BILAN ÉNERGÉTIQUE] Consommation : {emissions:.6f} kg CO2")