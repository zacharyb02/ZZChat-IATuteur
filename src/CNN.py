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
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4), # Augmenté pour éviter le surapprentissage sur 72 images
    layers.Dense(4, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement rapide de la tête
model.fit(train_ds, validation_data=val_ds, epochs=15)

