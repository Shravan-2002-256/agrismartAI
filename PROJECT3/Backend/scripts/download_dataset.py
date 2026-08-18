"""
Download and Prepare PlantVillage Dataset
"""
import os
import requests
import zipfile
from pathlib import Path
import shutil
from sklearn.model_selection import train_test_split
import random

# Dataset URL (PlantVillage from Kaggle)
DATASET_URL = "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/d5652a28-c1d8-4b76-97f3-72fb80f94efc/file_downloaded"

# Paths
DATA_DIR = "./data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

TRAIN_DIR = os.path.join(PROCESSED_DIR, "train")
VAL_DIR = os.path.join(PROCESSED_DIR, "validation")
TEST_DIR = os.path.join(PROCESSED_DIR, "test")

def create_directories():
    """Create necessary directories"""
    for directory in [RAW_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("Directories created successfully")

def download_dataset():
    """Download PlantVillage dataset"""
    print("Downloading PlantVillage dataset...")
    print("\nNOTE: Automated download may not work due to Kaggle restrictions.")
    print("Please download manually from:")
    print("https://www.kaggle.com/datasets/arjuntejaswi/plant-village")
    print("\nAlternatively, use Kaggle API:")
    print("kaggle datasets download -d arjuntejaswi/plant-village")
    print("\nAfter downloading, extract the zip file to:", RAW_DIR)
    print("\nFor this demo, we'll create sample data structure...")
    
    # Create sample disease classes for demonstration
    sample_classes = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___healthy',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
    ]
    
    for class_name in sample_classes:
        class_path = os.path.join(RAW_DIR, "PlantVillage", class_name)
        Path(class_path).mkdir(parents=True, exist_ok=True)
    
    print("\nSample data structure created.")
    print("Add images to the class folders or download full dataset.")

def split_dataset(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Split dataset into train, validation, and test sets"""
    
    plantvillage_dir = os.path.join(RAW_DIR, "PlantVillage")
    
    if not os.path.exists(plantvillage_dir):
        print(f"ERROR: PlantVillage directory not found at {plantvillage_dir}")
        print("Please download the dataset first.")
        return
    
    # Get all disease classes
    disease_classes = [d for d in os.listdir(plantvillage_dir) 
                      if os.path.isdir(os.path.join(plantvillage_dir, d))]
    
    print(f"\nFound {len(disease_classes)} disease classes")
    
    for disease_class in disease_classes:
        print(f"Processing {disease_class}...")
        
        # Get all images for this class
        class_path = os.path.join(plantvillage_dir, disease_class)
        images = [f for f in os.listdir(class_path) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if len(images) == 0:
            print(f"  No images found in {disease_class}, skipping...")
            continue
        
        # Shuffle images
        random.shuffle(images)
        
        # Calculate split sizes
        total = len(images)
        train_size = int(total * train_ratio)
        val_size = int(total * val_ratio)
        
        # Split images
        train_images = images[:train_size]
        val_images = images[train_size:train_size + val_size]
        test_images = images[train_size + val_size:]
        
        print(f"  Total: {total} | Train: {len(train_images)} | Val: {len(val_images)} | Test: {len(test_images)}")
        
        # Create class directories
        for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
            Path(os.path.join(split_dir, disease_class)).mkdir(parents=True, exist_ok=True)
        
        # Copy images to respective directories
        for img in train_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(TRAIN_DIR, disease_class, img)
            shutil.copy2(src, dst)
        
        for img in val_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(VAL_DIR, disease_class, img)
            shutil.copy2(src, dst)
        
        for img in test_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(TEST_DIR, disease_class, img)
            shutil.copy2(src, dst)
    
    print("\nDataset split completed successfully!")

def create_sample_images():
    """Create sample images for testing (colored squares)"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
    except ImportError:
        print("Pillow not installed. Skipping sample image creation.")
        return
    
    print("\nCreating sample images for testing...")
    
    plantvillage_dir = os.path.join(RAW_DIR, "PlantVillage")
    classes = [d for d in os.listdir(plantvillage_dir) 
              if os.path.isdir(os.path.join(plantvillage_dir, d))]
    
    for class_name in classes:
        class_path = os.path.join(plantvillage_dir, class_name)
        
        # Check if directory is empty
        existing_images = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if len(existing_images) > 0:
            continue
        
        # Create 10 sample images per class
        for i in range(10):
            # Create random colored image
            img = Image.new('RGB', (256, 256), 
                          color=(random.randint(50, 200), 
                                random.randint(50, 200), 
                                random.randint(50, 200)))
            
            # Add text
            draw = ImageDraw.Draw(img)
            text = f"{class_name[:15]}\n#{i+1}"
            draw.text((10, 10), text, fill=(255, 255, 255))
            
            # Save image
            img.save(os.path.join(class_path, f"sample_{i+1}.jpg"))
        
        print(f"Created 10 sample images for {class_name}")
    
    print("Sample images created successfully!")

if __name__ == "__main__":
    print("PlantVillage Dataset Download and Preparation")
    print("="*50)
    
    # Create directories
    create_directories()
    
    # Download dataset (manual step)
    download_dataset()
    
    # Create sample images for testing
    create_sample_images()
    
    # Ask user if they want to split the dataset
    print("\n" + "="*50)
    response = input("Have you added the dataset images? Split dataset now? (y/n): ")
    
    if response.lower() == 'y':
        split_dataset()
    else:
        print("\nTo split dataset later, run:")
        print("python scripts/download_dataset.py --split-only")
    
    print("\nSetup completed!")
    print("Dataset directory structure:")
    print(f"  Raw data: {RAW_DIR}")
    print(f"  Processed data: {PROCESSED_DIR}")
