"""
 Train Disease Detection Model using MobileNetV2
Real Training Pipeline with PlantVillage Dataset

This creates a model compatible with production disease detection service
"""
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path

# Configuration
IMG_SIZE = 224  # MobileNetV2 standard input
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Paths
DATA_DIR = "./data/processed"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "validation")
TEST_DIR = os.path.join(DATA_DIR, "test")

# Model save paths
MODELS_DIR = "./models"
Path(MODELS_DIR).mkdir(exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, f"disease_mobilenetv2_{TIMESTAMP}.h5")
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "disease_mobilenetv2_best.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

def create_mobilenetv2_model(num_classes):
    """
    Create disease detection model using MobileNetV2 from tf.keras.applications
    Transfer learning with frozen base + trainable classification head
    """
    print("\n🔨 Building MobileNetV2 Model...")
    print(f"   Feature Extractor: Keras MobileNetV2 (ImageNet)")
    print(f"   Input Size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"   Output Classes: {num_classes}")
    
    # Load pre-trained MobileNetV2 (without top classifier)
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,  # Remove classification head
        weights='imagenet',  # Pre-trained on ImageNet
        pooling='avg'  # Global average pooling
    )
    
    # Freeze the base model
    base_model.trainable = False
    
    # Build complete model with classification head
    inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3), name="input_image")
    
    # Feature extraction (frozen)
    x = base_model(inputs, training=False)
    
    # Classification head (trainable)
    x = layers.Dropout(0.3, name="dropout_1")(x)
    x = layers.Dense(512, activation='relu', name="dense_512")(x)
    x = layers.BatchNormalization(name="batch_norm_1")(x)
    x = layers.Dropout(0.3, name="dropout_2")(x)
    x = layers.Dense(256, activation='relu', name="dense_256")(x)
    x = layers.Dropout(0.2, name="dropout_3")(x)
    outputs = layers.Dense(num_classes, activation='softmax', name="disease_output")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="disease_detection_mobilenetv2")
    
    return model

def create_data_generators():
    """
    Create data generators with augmentation for training
    """
    print("\n📊 Creating Data Generators...")
    
    # Training data augmentation (helps model generalize)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # Validation and test (no augmentation, only rescaling)
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    # Load validation data
    val_generator = val_test_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    # Load test data
    test_generator = val_test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    print(f"   Training samples:   {train_generator.samples}")
    print(f"   Validation samples: {val_generator.samples}")
    print(f"   Test samples:       {test_generator.samples}")
    print(f"   Number of classes:  {train_generator.num_classes}")
    
    return train_generator, val_generator, test_generator

def train_model():
    """
    Main training function
    """
    print("="*70)
    print("🚀 Starting MobileNetV2 Disease Detection Training")
    print("="*70)
    
    # Check if data exists
    if not os.path.exists(TRAIN_DIR):
        print(f"\n❌ ERROR: Training data not found at {TRAIN_DIR}")
        print("   Run: python scripts/download_plantvillage_real.py")
        exit(1)
    
    # Create data generators
    train_gen, val_gen, test_gen = create_data_generators()
    num_classes = train_gen.num_classes
    
    # Save class indices for production use
    class_indices = train_gen.class_indices
    with open(CLASS_INDICES_PATH, 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"\n💾 Class indices saved to: {CLASS_INDICES_PATH}")
    
    # Create model
    model = create_mobilenetv2_model(num_classes)
    
    # Print model summary
    print("\n📋 Model Architecture:")
    model.summary()
    
    # Compile model
    print("\n⚙️  Compiling model...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )
    
    # Callbacks
    callbacks = [
        # Save best model
        ModelCheckpoint(
            BEST_MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        # Save checkpoint every epoch
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=False,
            verbose=0
        ),
        # Early stopping to prevent overfitting
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        # Reduce learning rate when plateaued
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        # TensorBoard removed (not installed)
    ]
    
    # Calculate steps
    steps_per_epoch = train_gen.samples // BATCH_SIZE
    validation_steps = val_gen.samples // BATCH_SIZE
    
    print("\n" + "="*70)
    print("📚 TRAINING PHASE: Training Classification Head")
    print("   (MobileNetV2 base is frozen)")
    print("="*70)
    
    # Train the model
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        steps_per_epoch=steps_per_epoch,
        validation_data=val_gen,
        validation_steps=validation_steps,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n" + "="*70)
    print("✅ Training Complete!")
    print("="*70)
    
    # Evaluate on test set
    print("\n" + "="*70)
    print("📊 Evaluating on Test Set")
    print("="*70)
    
    test_results = model.evaluate(test_gen, verbose=1)
    
    print("\n📈 Test Set Results:")
    print(f"   Loss:            {test_results[0]:.4f}")
    print(f"   Accuracy:        {test_results[1]:.4f} ({test_results[1]*100:.2f}%)")
    print(f"   Top-3 Accuracy:  {test_results[2]:.4f} ({test_results[2]*100:.2f}%)")
    print(f"   Precision:       {test_results[3]:.4f}")
    print(f"   Recall:          {test_results[4]:.4f}")
    
    # Save training history
    history_path = os.path.join(MODELS_DIR, f"training_history_{TIMESTAMP}.json")
    history_dict = {
        'history': {k: [float(v) for v in vals] for k, vals in history.history.items()},
        'test_results': {
            'loss': float(test_results[0]),
            'accuracy': float(test_results[1]),
            'top_3_accuracy': float(test_results[2]),
            'precision': float(test_results[3]),
            'recall': float(test_results[4])
        },
        'config': {
            'img_size': IMG_SIZE,
            'batch_size': BATCH_SIZE,
            'epochs': EPOCHS,
            'learning_rate': LEARNING_RATE,
            'num_classes': num_classes
        }
    }
    
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"\n💾 Training history saved to: {history_path}")
    print(f"💾 Best model saved to: {BEST_MODEL_PATH}")
    print(f"💾 Latest model saved to: {MODEL_SAVE_PATH}")
    
    # Print training summary
    print("\n" + "="*70)
    print("📊 Training Summary")
    print("="*70)
    print(f"   Best Val Accuracy:  {max(history.history['val_accuracy']):.4f}")
    print(f"   Final Train Acc:    {history.history['accuracy'][-1]:.4f}")
    print(f"   Final Val Acc:      {history.history['val_accuracy'][-1]:.4f}")
    print(f"   Test Accuracy:      {test_results[1]:.4f}")
    print(f"   Total Parameters:   {model.count_params():,}")
    
    print("\n" + "="*70)
    print("✅ ALL DONE!")
    print("="*70)
    print(f"\n🚀 Next Steps:")
    print(f"   1. Test the model:")
    print(f"      python ml_models/test_mobilenetv2_model.py")
    print(f"   2. Deploy to production:")
    print(f"      Copy {BEST_MODEL_PATH} to production directory")
    
    return model, history, test_results

if __name__ == "__main__":
    # Set seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Train model
    trained_model, training_history, test_metrics = train_model()
