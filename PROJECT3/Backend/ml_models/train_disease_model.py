"""
Train Disease Detection Model using EfficientNetB0 and PlantVillage Dataset
"""
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import numpy as np

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Paths
DATA_DIR = "./data/processed"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "validation")
TEST_DIR = os.path.join(DATA_DIR, "test")
MODEL_SAVE_PATH = "./models/disease_detection_efficientnet.h5"

def create_model(num_classes):
    """Create EfficientNetB0 model with custom top layers"""
    
    # Load pre-trained EfficientNetB0
    base_model = EfficientNetB0(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Create new model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model, base_model

def create_data_generators():
    """Create data generators with augmentation"""
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Validation and test data (no augmentation, only rescaling)
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load data
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    val_generator = val_test_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    test_generator = val_test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator, test_generator

def train_model():
    """Main training function"""
    
    print("Creating data generators...")
    train_gen, val_gen, test_gen = create_data_generators()
    
    num_classes = train_gen.num_classes
    print(f"Number of classes: {num_classes}")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    print(f"Test samples: {test_gen.samples}")
    
    # Create model
    print("\nCreating model...")
    model, base_model = create_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Phase 1: Train only top layers
    print("\n" + "="*50)
    print("PHASE 1: Training top layers (base model frozen)")
    print("="*50)
    
    history1 = model.fit(
        train_gen,
        epochs=20,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune last layers of base model
    print("\n" + "="*50)
    print("PHASE 2: Fine-tuning (unfreezing last 20 layers)")
    print("="*50)
    
    # Unfreeze last 20 layers
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    # Re-compile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    history2 = model.fit(
        train_gen,
        epochs=30,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    print("\n" + "="*50)
    print("Evaluating on test set...")
    print("="*50)
    
    test_loss, test_acc, test_top3 = model.evaluate(test_gen, verbose=1)
    print(f"\nTest accuracy: {test_acc:.4f}")
    print(f"Test top-3 accuracy: {test_top3:.4f}")
    print(f"Test loss: {test_loss:.4f}")
    
    # Save final model
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved to {MODEL_SAVE_PATH}")
    
    # Save class indices
    import json
    class_indices = train_gen.class_indices
    with open("./models/class_indices.json", "w") as f:
        json.dump(class_indices, f, indent=2)
    print("Class indices saved")
    
    return model, history1, history2

if __name__ == "__main__":
    print("Starting Disease Detection Model Training")
    print("="*50)
    
    # Check if data exists
    if not os.path.exists(TRAIN_DIR):
        print(f"\nERROR: Training data not found at {TRAIN_DIR}")
        print("Please run 'python scripts/download_dataset.py' first")
        exit(1)
    
    # Train model
    model, hist1, hist2 = train_model()
    
    print("\nTraining completed successfully!")
