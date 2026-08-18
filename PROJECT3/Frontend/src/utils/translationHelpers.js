/**
 * Frontend Translation Utilities
 * Provides helper functions for translating dynamic content
 */

export const translateCropName = (cropName, t) => {
  if (!cropName) return cropName;
  
  const cropKey = `crop_${cropName.toLowerCase()}`;
  const translated = t(cropKey);
  
  // If translation not found, return capitalized original
  if (translated === cropKey) {
    return cropName.charAt(0).toUpperCase() + cropName.slice(1);
  }
  
  return translated;
};

export const translateDiseaseName = (diseaseName, t) => {
  if (!diseaseName) return diseaseName;
  
  const diseaseMap = {
    'Healthy': 'disease_healthy',
    'Healthy Plants': 'disease_healthy_plants',
    'Leaf Spot': 'disease_leaf_spot',
    'Leaf Spot Disease': 'disease_leaf_spot',
    'Tomato Late Blight': 'disease_late_blight',
    'Tomato Early Blight': 'disease_early_blight',
    'Powdery Mildew': 'disease_powdery_mildew',
    'Bacterial Spot': 'disease_bacterial_spot',
    'Blight': 'disease_blight',
  };
  
  const key = diseaseMap[diseaseName] || `disease_${diseaseName.toLowerCase().replace(/\s+/g, '_')}`;
  const translated = t(key);
  
  // If translation not found, return original
  if (translated === key) {
    return diseaseName;
  }
  
  return translated;
};

export const translateSeverity = (severity, t) => {
  if (!severity) return severity;
  
  const severityMap = {
    'none': 'severity_none',
    'low': 'severity_low',
    'medium': 'severity_medium',
    'moderate': 'severity_medium',
    'high': 'severity_high',
    'critical': 'severity_high',
  };
  
  const key = severityMap[severity.toLowerCase()] || severity;
  return t(key);
};

export const getCropOptions = (cropTypes, t) => {
  return cropTypes.map(crop => ({
    value: crop,
    label: translateCropName(crop, t)
  }));
};
