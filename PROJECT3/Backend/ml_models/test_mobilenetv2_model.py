"""
Test and Evaluate MobileNetV2 Disease Detection Model
Comprehensive testing including:
- Accuracy metrics
- Confusion matrix
- Per-class performance
- Inference time
- Sample predictions
"""
import tensorflow as tf
import numpy as np
import json
import os
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import time
from PIL import Image

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32

# Paths
MODELS_DIR = "./models"
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "disease_mobilenetv2_best.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")
TEST_DIR = "./data/processed/test"

# Results directory
RESULTS_DIR = "./test_results"
Path(RESULTS_DIR).mkdir(exist_ok=True)

def load_model_and_classes():
    """Load trained model and class mappings"""
    print(" Loading model...")
    
    if not os.path.exists(BEST_MODEL_PATH):
        print(f"  Model not found at: {BEST_MODEL_PATH}")
        print("   Please train the model first:")
        print("   python ml_models/train_mobilenetv2_disease_model.py")
        exit(1)
    
    # Load model (standard Keras model, no custom objects needed)
    model = tf.keras.models.load_model(BEST_MODEL_PATH)
    
    print(" Model loaded successfully")
    print(f"   Parameters: {model.count_params():,}")
    
    # Load class indices
    if os.path.exists(CLASS_INDICES_PATH):
        with open(CLASS_INDICES_PATH, 'r') as f:
            class_indices = json.load(f)
        # Create reverse mapping (index -> class name)
        index_to_class = {v: k for k, v in class_indices.items()}
    else:
        print("  Class indices file not found, will use numeric indices")
        index_to_class = None
    
    return model, index_to_class

def create_test_generator():
    """Create test data generator"""
    print("\n Loading test data...")
    
    if not os.path.exists(TEST_DIR):
        print(f" Test data not found at: {TEST_DIR}")
        exit(1)
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False  # Important for correct label alignment
    )
    
    print(f"   Test samples: {test_generator.samples}")
    print(f"   Classes: {test_generator.num_classes}")
    
    return test_generator

def evaluate_model(model, test_gen):
    """
    Comprehensive model evaluation
    """
    print("\n" + "="*70)
    print(" EVALUATING MODEL")
    print("="*70)
    
    # Basic evaluation
    print("\n Computing metrics...")
    test_results = model.evaluate(test_gen, verbose=1)
    
    print("\n Test Set Performance:")
    print(f"   Loss:            {test_results[0]:.4f}")
    print(f"   Accuracy:        {test_results[1]:.4f} ({test_results[1]*100:.2f}%)")
    print(f"   Top-3 Accuracy:  {test_results[2]:.4f} ({test_results[2]*100:.2f}%)")
    print(f"   Precision:       {test_results[3]:.4f}")
    print(f"   Recall:          {test_results[4]:.4f}")
    
    # Get predictions
    print("\n Generating predictions...")
    test_gen.reset()
    predictions = model.predict(test_gen, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Get true labels
    true_classes = test_gen.classes
    class_labels = list(test_gen.class_indices.keys())
    
    print(f"   Total predictions: {len(predicted_classes)}")
    
    return {
        'predictions': predictions,
        'predicted_classes': predicted_classes,
        'true_classes': true_classes,
        'class_labels': class_labels,
        'metrics': test_results
    }

def generate_classification_report(results):
    """Generate detailed classification report"""
    print("\n" + "="*70)
    print(" PER-CLASS PERFORMANCE")
    print("="*70)
    
    report = classification_report(
        results['true_classes'],
        results['predicted_classes'],
        target_names=results['class_labels'],
        digits=4
    )
    
    print(report)
    
    # Save to file
    report_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n💾 Report saved to: {report_path}")
    
    return report

def plot_confusion_matrix(results):
    """Generate and save confusion matrix"""
    print("\n" + "="*70)
    print(" CONFUSION MATRIX")
    print("="*70)
    
    cm = confusion_matrix(results['true_classes'], results['predicted_classes'])
    
    # Calculate per-class accuracy
    class_accuracy = cm.diagonal() / cm.sum(axis=1)
    
    print("\n📈 Per-Class Accuracy:")
    for idx, (label, acc) in enumerate(zip(results['class_labels'], class_accuracy)):
        print(f"   {label:40s}: {acc:.4f} ({acc*100:.2f}%)")
    
    # Plot confusion matrix
    plt.figure(figsize=(20, 16))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=results['class_labels'],
        yticklabels=results['class_labels'],
        cbar_kws={'label': 'Number of Predictions'}
    )
    plt.title('Confusion Matrix - Disease Detection Model', fontsize=16, pad=20)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    cm_path = os.path.join(RESULTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=150, bbox_inches='tight')
    print(f"\n Confusion matrix saved to: {cm_path}")
    plt.close()

def measure_inference_time(model):
    """Measure inference time"""
    print("\n" + "="*70)
    print(" INFERENCE TIME TEST")
    print("="*70)
    
    # Create dummy input
    dummy_input = np.random.rand(1, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    
    # Warm-up
    _ = model.predict(dummy_input, verbose=0)
    
    # Measure
    times = []
    num_runs = 100
    
    print(f"\n   Running {num_runs} inference iterations...")
    for _ in range(num_runs):
        start = time.time()
        _ = model.predict(dummy_input, verbose=0)
        times.append((time.time() - start) * 1000)  # Convert to ms
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    min_time = np.min(times)
    max_time = np.max(times)
    
    print(f"\n Inference Time Statistics:")
    print(f"   Average: {avg_time:.2f} ms")
    print(f"   Std Dev: {std_time:.2f} ms")
    print(f"   Min:     {min_time:.2f} ms")
    print(f"   Max:     {max_time:.2f} ms")
    print(f"   FPS:     {1000/avg_time:.1f} frames/second")
    
    return {
        'avg_ms': avg_time,
        'std_ms': std_time,
        'min_ms': min_time,
        'max_ms': max_time,
        'fps': 1000/avg_time
    }

def test_sample_predictions(model, test_gen, num_samples=10):
    """Test sample predictions with confidence scores"""
    print("\n" + "="*70)
    print(" SAMPLE PREDICTIONS")
    print("="*70)
    
    test_gen.reset()
    
    # Get a batch
    images, labels = next(test_gen)
    
    # Predict
    predictions = model.predict(images[:num_samples], verbose=0)
    
    print(f"\n   Showing {num_samples} sample predictions:\n")
    
    for i in range(min(num_samples, len(images))):
        true_idx = np.argmax(labels[i])
        pred_idx = np.argmax(predictions[i])
        confidence = predictions[i][pred_idx] * 100
        
        true_label = test_gen.class_indices
        true_label = {v: k for k, v in true_label.items()}[true_idx]
        pred_label = {v: k for k, v in test_gen.class_indices.items()}[pred_idx]
        
        status = "✅" if true_idx == pred_idx else "❌"
        
        print(f"   {status} Sample {i+1}:")
        print(f"      True:       {true_label}")
        print(f"      Predicted:  {pred_label}")
        print(f"      Confidence: {confidence:.2f}%")
        print()

def save_test_summary(results, inference_times):
    """Save comprehensive test summary"""
    summary = {
        'test_metrics': {
            'loss': float(results['metrics'][0]),
            'accuracy': float(results['metrics'][1]),
            'top_3_accuracy': float(results['metrics'][2]),
            'precision': float(results['metrics'][3]),
            'recall': float(results['metrics'][4])
        },
        'inference_performance': inference_times,
        'dataset_info': {
            'num_classes': len(results['class_labels']),
            'total_test_samples': len(results['true_classes']),
            'classes': results['class_labels']
        }
    }
    
    summary_path = os.path.join(RESULTS_DIR, "test_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n Test summary saved to: {summary_path}")

def main():
    """Main testing pipeline"""
    print("="*70)
    print(" MobileNetV2 Disease Detection Model - Testing & Evaluation")
    print("="*70)
    
    # Load model
    model, index_to_class = load_model_and_classes()
    
    # Load test data
    test_gen = create_test_generator()
    
    # Evaluate model
    results = evaluate_model(model, test_gen)
    
    # Generate classification report
    generate_classification_report(results)
    
    # Plot confusion matrix
    plot_confusion_matrix(results)
    
    # Measure inference time
    inference_times = measure_inference_time(model)
    
    # Test sample predictions
    test_sample_predictions(model, test_gen, num_samples=10)
    
    # Save summary
    save_test_summary(results, inference_times)
    
    print("\n" + "="*70)
    print(" TESTING COMPLETE!")
    print("="*70)
    print(f"\n Results saved to: {os.path.abspath(RESULTS_DIR)}")
    print(f"\n Key Metrics:")
    print(f"   Test Accuracy:  {results['metrics'][1]*100:.2f}%")
    print(f"   Inference Time: {inference_times['avg_ms']:.2f} ms")
    print(f"   Throughput:     {inference_times['fps']:.1f} FPS")
    
    print("\n FOR VIVA PRESENTATION:")
    print("   - Model uses MobileNetV2 transfer learning (3.4M params)")
    print("   - Trained on PlantVillage dataset")
    print(f"   - Achieves {results['metrics'][1]*100:.2f}% accuracy on test set")
    print(f"   - Real-time inference: {inference_times['avg_ms']:.2f}ms per image")
    print(f"   - Detects {len(results['class_labels'])} disease classes")

if __name__ == "__main__":
    main()
