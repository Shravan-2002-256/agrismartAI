"""
Model inference service for crop disease detection.

Priority order:
1) Real trained model inference (if TensorFlow + model artifact are available)
2) Feature-based fallback (deterministic CV heuristics)
"""

from __future__ import annotations

import io
import json
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from PIL import Image

from app.core.config import settings


@dataclass
class InferenceResult:
    disease: str
    confidence: float
    method: str
    model_version: str
    raw_label: str
    uncertain: bool
    inference_ms: int


class ModelInferenceService:
    def __init__(self) -> None:
        self._load_attempted = False
        self._model = None
        self._tf = None
        self._idx_to_label: Dict[int, str] = {}
        self._status_reason = "not_initialized"

    def _lazy_load(self) -> None:
        if self._load_attempted:
            return
        self._load_attempted = True

        # Load optional class mapping first.
        class_map_path = "./models/class_indices.json"
        if os.path.exists(class_map_path):
            try:
                with open(class_map_path, "r", encoding="utf-8") as f:
                    class_to_idx = json.load(f)
                self._idx_to_label = {int(v): str(k) for k, v in class_to_idx.items()}
            except Exception:
                self._idx_to_label = {}

        # Load TensorFlow model only if available in environment.
        try:
            import tensorflow as tf  # type: ignore

            self._tf = tf
            if os.path.exists(settings.MODEL_PATH):
                self._model = tf.keras.models.load_model(settings.MODEL_PATH)
                self._status_reason = "model_loaded"
            else:
                self._status_reason = "model_file_missing"
        except Exception:
            self._model = None
            self._tf = None
            self._status_reason = "tensorflow_or_model_unavailable"

    def status(self) -> Dict:
        self._lazy_load()
        return {
            "model_loaded": self._model is not None,
            "reason": self._status_reason,
            "model_path": settings.MODEL_PATH,
            "class_map_loaded": len(self._idx_to_label) > 0,
            "input_size": settings.MODEL_INPUT_SIZE,
            "confidence_threshold": settings.DISEASE_CONFIDENCE_THRESHOLD,
        }

    def _preprocess(self, image_bytes: bytes) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((settings.MODEL_INPUT_SIZE, settings.MODEL_INPUT_SIZE))
        arr = np.asarray(image, dtype=np.float32) / 255.0
        return np.expand_dims(arr, axis=0)

    def _normalize_label(self, raw_label: str, crop_type: str) -> str:
        label = raw_label.lower().replace("__", " ").replace("_", " ")
        if "healthy" in label:
            return "Healthy"
        if "late blight" in label:
            return "Tomato Late Blight"
        if "early blight" in label:
            return "Tomato Early Blight"
        if "bacterial spot" in label:
            return "Bacterial Spot"
        if "powdery mildew" in label:
            return "Powdery Mildew"

        # Conservative fallback keeps behavior aligned with supported knowledge base.
        crop = (crop_type or "").lower()
        if crop in {"tomato", "potato"}:
            return "Tomato Early Blight"
        return "Powdery Mildew"

    def _heuristic_predict(self, image_bytes: bytes, crop_type: str) -> InferenceResult:
        t0 = time.time()
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((224, 224))
        arr = np.asarray(image, dtype=np.float32)

        avg = np.mean(arr, axis=(0, 1))
        green_ratio = float(avg[1] / (avg.sum() + 1e-6))

        brown_pixels = np.sum((arr[:, :, 0] > 100) & (arr[:, :, 1] < 150) & (arr[:, :, 2] < 100))
        yellow_pixels = np.sum((arr[:, :, 0] > 190) & (arr[:, :, 1] > 170) & (arr[:, :, 2] < 150))
        total = 224 * 224
        brown_ratio = float(brown_pixels / total)
        yellow_ratio = float(yellow_pixels / total)

        if green_ratio > 0.36 and brown_ratio < 0.04 and yellow_ratio < 0.04:
            disease, conf = "Healthy", 0.86
        elif brown_ratio > 0.14:
            disease, conf = "Tomato Late Blight", 0.78
        elif brown_ratio > 0.08:
            disease, conf = "Tomato Early Blight", 0.74
        elif yellow_ratio > 0.12:
            disease, conf = "Bacterial Spot", 0.72
        else:
            disease, conf = "Powdery Mildew", 0.69

        # Crop-aware fallback consistency
        crop = (crop_type or "").lower()
        if crop in {"pepper"} and disease in {"Tomato Early Blight", "Tomato Late Blight"}:
            disease = "Bacterial Spot"

        uncertain = conf < settings.DISEASE_CONFIDENCE_THRESHOLD
        return InferenceResult(
            disease=disease,
            confidence=conf,
            method="feature_fallback",
            model_version="heuristic-v1",
            raw_label=disease,
            uncertain=uncertain,
            inference_ms=int((time.time() - t0) * 1000),
        )

    def predict(self, image_bytes: bytes, crop_type: str = "tomato") -> InferenceResult:
        self._lazy_load()
        t0 = time.time()

        if self._model is not None and self._tf is not None:
            arr = self._preprocess(image_bytes)
            probs = self._model.predict(arr, verbose=0)
            probs = probs[0] if getattr(probs, "ndim", 1) > 1 else probs

            class_idx = int(np.argmax(probs))
            conf = float(probs[class_idx])
            raw = self._idx_to_label.get(class_idx, f"class_{class_idx}")
            disease = self._normalize_label(raw, crop_type)
            uncertain = conf < settings.DISEASE_CONFIDENCE_THRESHOLD

            return InferenceResult(
                disease=disease,
                confidence=conf,
                method="trained_model",
                model_version="efficientnetb0-transfer-v1",
                raw_label=raw,
                uncertain=uncertain,
                inference_ms=int((time.time() - t0) * 1000),
            )

        return self._heuristic_predict(image_bytes, crop_type)


model_inference_service = ModelInferenceService()
