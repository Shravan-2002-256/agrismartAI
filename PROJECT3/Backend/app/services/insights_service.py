"""
Insights Service
Analyzes detection patterns and generates actionable insights
"""
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Any
from app.models.detection import Detection
from app.utils.translations import translate, translate_crop_name, translate_disease_name


class InsightsService:
    """Service for generating insights from detection data"""
    
    # Disease remedies knowledge base
    DISEASE_REMEDIES = {
        'leaf_spot': {
            'disease_name': 'Leaf Spot Disease',
            'description': 'Fungal infection causing spots on leaves',
            'causes': ['High humidity', 'Overhead watering', 'Poor air circulation'],
            'remedies': [
                'Remove and destroy affected leaves immediately',
                'Apply copper-based fungicide (Copper oxychloride 50% WP @ 3g/liter)',
                'Use Mancozeb 75% WP @ 2.5g/liter as preventive spray',
                'Spray Chlorothalonil 75% WP @ 2g/liter every 7-10 days',
                'Ensure proper spacing between plants for air circulation'
            ],
            'fertilizer_recommendations': [
                'Apply balanced NPK (19:19:19) @ 2g/liter',
                'Add potassium fertilizer to strengthen plant immunity',
                'Use micronutrient spray with Zinc and Manganese'
            ],
            'prevention': [
                'Avoid overhead watering - use drip irrigation',
                'Water in the morning to allow leaves to dry',
                'Maintain proper plant spacing (18-24 inches)',
                'Remove crop debris and weeds regularly',
                'Apply organic mulch to prevent soil splash'
            ]
        },
        'blight': {
            'disease_name': 'Blight (Early/Late Blight)',
            'description': 'Fungal disease affecting leaves, stems, and fruits',
            'causes': ['Cool, wet weather', 'Poor drainage', 'Infected seed/transplants'],
            'remedies': [
                'Apply Metalaxyl + Mancozeb @ 2.5g/liter at first sign',
                'Use Bordeaux mixture (1%) for organic control',
                'Spray Azoxystrobin 23% SC @ 1ml/liter',
                'Apply Dimethomorph 50% WP @ 1.5g/liter for late blight',
                'Remove and burn severely infected plants'
            ],
            'fertilizer_recommendations': [
                'Increase calcium application - Calcium nitrate @ 2g/liter',
                'Apply NPK 12:32:16 @ 3g/liter for stronger stems',
                'Use foliar spray with Calcium chloride (0.5%)'
            ],
            'prevention': [
                'Use disease-resistant varieties',
                'Rotate crops - avoid planting in same location for 3 years',
                'Stake plants to improve air circulation',
                'Apply preventive fungicide sprays during humid weather',
                'Remove volunteer plants that can harbor disease'
            ]
        },
        'powdery_mildew': {
            'disease_name': 'Powdery Mildew',
            'description': 'White powdery fungal growth on leaves',
            'causes': ['Moderate temperature', 'High humidity', 'Dense planting'],
            'remedies': [
                'Apply Sulfur 80% WP @ 3g/liter (organic option)',
                'Spray Triadimefon 25% WP @ 0.5ml/liter',
                'Use Hexaconazole 5% SC @ 2ml/liter',
                'Apply Potassium bicarbonate solution (5g/liter)',
                'Spray neem oil (3ml/liter) weekly for organic control'
            ],
            'fertilizer_recommendations': [
                'Avoid high nitrogen fertilizers during infection',
                'Apply balanced NPK 15:15:15 @ 2g/liter',
                'Use silicon-based fertilizer to strengthen plant cell walls'
            ],
            'prevention': [
                'Plant in full sun with good air circulation',
                'Avoid over-fertilizing with nitrogen',
                'Water at soil level, not on leaves',
                'Prune infected leaves immediately',
                'Apply preventive sulfur spray bi-weekly'
            ]
        },
        'bacterial_wilt': {
            'disease_name': 'Bacterial Wilt',
            'description': 'Bacterial infection causing sudden wilting and plant death',
            'causes': ['Soil-borne bacteria', 'Insect damage', 'Contaminated tools'],
            'remedies': [
                'Remove and burn infected plants immediately',
                'Apply Streptocycline 90% SP + Copper oxychloride @ 1g + 3g/liter',
                'Drench soil with Bleaching powder solution (10g/liter)',
                'Use Pseudomonas fluorescens @ 10g/liter as biological control',
                'Treat soil with Trichoderma viride @ 5g/liter'
            ],
            'fertilizer_recommendations': [
                'Apply calcium-rich fertilizer to strengthen cell walls',
                'Use organic compost to improve soil health',
                'Apply biofertilizers with beneficial bacteria'
            ],
            'prevention': [
                'Use certified disease-free seeds and transplants',
                'Sterilize tools between plants',
                'Control cucumber beetles and other vectors',
                'Improve soil drainage',
                'Practice crop rotation with non-susceptible crops'
            ]
        },
        'anthracnose': {
            'disease_name': 'Anthracnose',
            'description': 'Fungal disease causing dark lesions on fruits and leaves',
            'causes': ['Warm, humid conditions', 'Overhead irrigation', 'Crop debris'],
            'remedies': [
                'Apply Copper fungicide @ 3g/liter',
                'Spray Carbendazim 50% WP @ 1g/liter',
                'Use Azoxystrobin 23% SC @ 1ml/liter',
                'Apply Mancozeb 75% WP @ 2.5g/liter preventively',
                'Remove infected fruits and leaves immediately'
            ],
            'fertilizer_recommendations': [
                'Use balanced NPK 10:26:26 @ 2.5g/liter',
                'Apply potassium-rich fertilizer for fruit strength',
                'Add micronutrients especially Boron and Calcium'
            ],
            'prevention': [
                'Use drip irrigation instead of overhead watering',
                'Mulch to prevent soil splash on fruits',
                'Harvest mature fruits promptly',
                'Clean up and destroy crop residues after harvest',
                'Space plants adequately for air circulation'
            ]
        },
        'mosaic_virus': {
            'disease_name': 'Mosaic Virus',
            'description': 'Viral infection causing mottled yellow/green leaf patterns',
            'causes': ['Aphids and other sap-sucking insects', 'Infected transplants', 'Mechanical transmission'],
            'remedies': [
                'Remove and destroy infected plants immediately (no cure for viral diseases)',
                'Control aphid vectors with Imidacloprid 17.8% SL @ 0.5ml/liter',
                'Spray Acetamiprid 20% SP @ 0.5g/liter for insect control',
                'Use yellow sticky traps to monitor and trap aphids',
                'Apply neem oil @ 5ml/liter to repel insects'
            ],
            'fertilizer_recommendations': [
                'Boost plant immunity with NPK 19:19:19 @ 2g/liter',
                'Apply micronutrient spray (Zinc, Iron, Manganese)',
                'Use seaweed extract to improve plant vigor'
            ],
            'prevention': [
                'Use virus-resistant varieties when available',
                'Start with certified virus-free transplants',
                'Control aphids and whiteflies from early growth',
                'Remove weeds that can harbor viruses',
                'Avoid working with plants when wet',
                'Disinfect tools regularly'
            ]
        },
        'rust': {
            'disease_name': 'Rust Disease',
            'description': 'Fungal disease causing orange-brown pustules on leaves',
            'causes': ['High humidity', 'Moderate temperatures', 'Dense canopy'],
            'remedies': [
                'Apply Mancozeb 75% WP @ 2.5g/liter',
                'Spray Propiconazole 25% EC @ 1ml/liter',
                'Use Sulfur 80% WP @ 3g/liter for organic control',
                'Apply Triadimefon 25% WP @ 1g/liter',
                'Remove severely infected leaves'
            ],
            'fertilizer_recommendations': [
                'Apply balanced NPK 12:12:17 @ 2g/liter',
                'Increase potassium levels for disease resistance',
                'Use micronutrient spray with Zinc and Boron'
            ],
            'prevention': [
                'Plant resistant varieties',
                'Ensure good air circulation between plants',
                'Avoid overhead irrigation',
                'Apply preventive fungicide during humid weather',
                'Remove and destroy infected plant debris'
            ]
        },
        'healthy': {
            'disease_name': 'Healthy Plants',
            'description': 'No disease detected - plants are in good condition',
            'causes': [],
            'remedies': [
                'Continue regular monitoring',
                'Maintain current care practices'
            ],
            'fertilizer_recommendations': [
                'Apply balanced NPK 19:19:19 @ 2g/liter every 15 days',
                'Use organic compost or vermicompost @ 100g/plant monthly',
                'Apply micronutrient spray once a month'
            ],
            'prevention': [
                'Monitor plants regularly for early disease detection',
                'Maintain proper watering schedule',
                'Ensure adequate spacing and air circulation',
                'Remove any yellowing or damaged leaves',
                'Keep growing area clean and weed-free'
            ]
        }
    }
    
    @staticmethod
    def get_weekly_insights(db, user_id: int = None, days: int = 7, language: str = 'en') -> Dict[str, Any]:
        """
        Analyze last N days of detections and generate insights
        
        Args:
            db: Database session
            user_id: Specific user ID or None for all users
            days: Number of days to analyze (default 7)
            language: Language code for translations (en, hi, te, ta)
            
        Returns:
            Dictionary with insights and recommendations
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query detections
        query = db.query(Detection).filter(
            Detection.detected_at >= start_date,
            Detection.detected_at <= end_date
        )
        
        if user_id:
            query = query.filter(Detection.user_id == user_id)
        
        detections = query.all()
        
        if not detections:
            return {
                'period': f'Last {days} days',
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'total_detections': 0,
                'insights': [],
                'message': 'No detections found in this period. Upload crop images to get insights!'
            }
        
        # Analyze detections
        analysis = InsightsService._analyze_detections(detections)
        
        # Generate insights with translations
        insights = InsightsService._generate_insights(analysis, language)
        
        return {
            'period': f'Last {days} days',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_detections': len(detections),
            'total_crops': analysis['total_crops'],
            'crop_breakdown': analysis['crop_breakdown'],
            'insights': insights,
            'summary': InsightsService._generate_summary(analysis, language)
        }
    
    @staticmethod
    def _analyze_detections(detections: List[Detection]) -> Dict[str, Any]:
        """Analyze detection patterns"""
        crop_data = defaultdict(lambda: {
            'count': 0,
            'diseases': [],
            'healthy_count': 0,
            'diseased_count': 0,
            'avg_confidence': []
        })
        
        for detection in detections:
            crop = detection.crop_type or 'Unknown'
            disease = detection.disease_detected.lower()
            confidence = detection.confidence
            
            crop_data[crop]['count'] += 1
            crop_data[crop]['diseases'].append(disease)
            crop_data[crop]['avg_confidence'].append(confidence)
            
            if 'healthy' in disease:
                crop_data[crop]['healthy_count'] += 1
            else:
                crop_data[crop]['diseased_count'] += 1
        
        # Calculate statistics
        crop_breakdown = []
        for crop, data in crop_data.items():
            disease_counter = Counter(data['diseases'])
            most_common_diseases = disease_counter.most_common(3)
            
            crop_breakdown.append({
                'crop_type': crop,
                'total_uploads': data['count'],
                'healthy_count': data['healthy_count'],
                'diseased_count': data['diseased_count'],
                'disease_rate': round((data['diseased_count'] / data['count']) * 100, 1),
                'most_common_diseases': [
                    {
                        'disease': disease,
                        'count': count,
                        'percentage': round((count / data['count']) * 100, 1)
                    }
                    for disease, count in most_common_diseases
                ],
                'avg_confidence': round(sum(data['avg_confidence']) / len(data['avg_confidence']), 1)
            })
        
        # Sort by upload count
        crop_breakdown.sort(key=lambda x: x['total_uploads'], reverse=True)
        
        return {
            'total_crops': len(crop_data),
            'crop_breakdown': crop_breakdown
        }
    
    @staticmethod
    def _generate_insights(analysis: Dict[str, Any], language: str = 'en') -> List[Dict[str, Any]]:
        """Generate actionable insights with remedies"""
        insights = []
        
        for crop_data in analysis['crop_breakdown']:
            crop = crop_data['crop_type']
            total = crop_data['total_uploads']
            diseased = crop_data['diseased_count']
            healthy = crop_data['healthy_count']
            disease_rate = crop_data['disease_rate']
            most_common = crop_data['most_common_diseases']
            
            if not most_common:
                continue
            
            # Generate insight for each crop
            primary_disease = most_common[0]
            disease_name = primary_disease['disease']
            disease_count = primary_disease['count']
            disease_percentage = primary_disease['percentage']
            
            # Determine severity level
            if disease_rate >= 70:
                severity = 'critical'
                urgency = translate('immediate_action_required', language)
            elif disease_rate >= 40:
                severity = 'high'
                urgency = translate('action_needed_soon', language)
            elif disease_rate >= 20:
                severity = 'moderate'
                urgency = translate('keep_monitoring', language)
            else:
                severity = 'low'
                urgency = translate('keep_monitoring', language)
            
            # Get remedies from knowledge base
            remedies_data = InsightsService._get_remedies(disease_name)
            
            # Translate crop and disease names
            translated_crop = translate_crop_name(crop, language)
            translated_disease = translate_disease_name(remedies_data['disease_name'], language)
            
            # Create insight
            insight = {
                'crop_type': translated_crop,
                'crop_type_original': crop,
                'total_uploads': total,
                'diseased_count': diseased,
                'healthy_count': healthy,
                'disease_rate': disease_rate,
                'severity': severity,
                'urgency': urgency,
                'primary_disease': {
                    'name': disease_name,
                    'count': disease_count,
                    'percentage': disease_percentage,
                    'display_name': translated_disease
                },
                'pattern_description': InsightsService._create_pattern_description(
                    translated_crop, disease_percentage, translated_disease, diseased, healthy, total, language
                ),
                'remedies': InsightsService._translate_remedies(remedies_data.get('remedies', []), language),
                'fertilizer_recommendations': InsightsService._translate_fertilizers(remedies_data.get('fertilizer_recommendations', []), language),
                'prevention_tips': InsightsService._translate_prevention(remedies_data.get('prevention', []), language),
                'causes': remedies_data.get('causes', []),
                'other_diseases': [
                    {
                        'name': d['disease'],
                        'count': d['count'],
                        'percentage': d['percentage']
                    }
                    for d in most_common[1:3]
                ] if len(most_common) > 1 else []
            }
            
            insights.append(insight)
        
        return insights
    
    @staticmethod
    def _get_remedies(disease_name: str) -> Dict[str, Any]:
        """Get remedies for a disease from knowledge base"""
        # Normalize disease name
        disease_key = disease_name.lower().replace(' ', '_')
        
        # Try to find in knowledge base
        for key, data in InsightsService.DISEASE_REMEDIES.items():
            if key in disease_key or disease_key in key:
                return data
        
        # Default for unknown diseases
        return {
            'disease_name': disease_name.title(),
            'description': 'Disease detected',
            'causes': ['Various environmental and biological factors'],
            'remedies': [
                'Consult local agricultural expert for specific treatment',
                'Remove and destroy affected plant parts',
                'Apply broad-spectrum fungicide as preventive measure',
                'Improve plant health with proper nutrition and watering'
            ],
            'fertilizer_recommendations': [
                'Apply balanced NPK fertilizer (19:19:19) @ 2g/liter',
                'Use micronutrient spray to boost plant immunity'
            ],
            'prevention': [
                'Monitor plants regularly',
                'Maintain proper spacing and air circulation',
                'Practice crop rotation',
                'Keep growing area clean'
            ]
        }
    
    @staticmethod
    def _create_pattern_description(crop: str, percentage: float, disease: str, 
                                   diseased: int, healthy: int, total: int, language: str = 'en') -> str:
        """Create human-readable pattern description"""
        if 'healthy' in disease.lower() or 'ఆరోగ్యకరమైన' in disease or 'स्वस्थ' in disease or 'ஆரோக்கியமான' in disease:
            return translate('healthy_message', language, 
                           percent=round((healthy / total) * 100, 1), 
                           crop=crop, 
                           healthy=healthy, 
                           total=total)
        
        if percentage >= 70:
            return translate('critical_alert', language,
                           percent=percentage,
                           crop=crop,
                           diseased=diseased,
                           total=total,
                           disease=disease)
        elif percentage >= 50:
            return translate('critical_alert', language,
                           percent=percentage,
                           crop=crop,
                           diseased=diseased,
                           total=total,
                           disease=disease)
        elif percentage >= 30:
            return translate('critical_alert', language,
                           percent=percentage,
                           crop=crop,
                           diseased=diseased,
                           total=total,
                           disease=disease)
        else:
            return translate('healthy_message', language,
                           percent=round((healthy / total) * 100, 1), 
                           crop=crop, 
                           healthy=healthy, 
                           total=total)
    
    @staticmethod
    def _generate_summary(analysis: Dict[str, Any], language: str = 'en') -> str:
        """Generate overall summary"""
        if analysis['total_crops'] == 0:
            return "No data available for analysis."
        
        total_diseased = sum(crop['diseased_count'] for crop in analysis['crop_breakdown'])
        total_uploads = sum(crop['total_uploads'] for crop in analysis['crop_breakdown'])
        
        if total_diseased == 0:
            return translate('health_status_low', language, percent=0.0)
        
        disease_rate = round((total_diseased / total_uploads) * 100, 1)
        crop_count = analysis['total_crops']
        
        if disease_rate >= 50:
            return translate('health_status_critical', language, percent=disease_rate)
        elif disease_rate >= 25:
            return translate('health_status_moderate', language, percent=disease_rate, crop_count=crop_count)
        else:
            return translate('health_status_low', language, percent=disease_rate)
    
    @staticmethod
    def _translate_remedies(remedies: List[str], language: str = 'en') -> List[str]:
        """Translate remedy recommendations"""
        if language == 'en':
            return remedies
        
        translated = []
        for remedy in remedies:
            # Try to match with known translation keys
            remedy_lower = remedy.lower()
            if 'continue' in remedy_lower and 'monitor' in remedy_lower:
                translated.append(translate('continue_monitoring', language))
            elif 'maintain' in remedy_lower and 'practice' in remedy_lower:
                translated.append(translate('maintain_practices', language))
            elif 'remove' in remedy_lower and 'affected' in remedy_lower:
                translated.append(translate('remove_affected', language))
            elif 'fungicide' in remedy_lower:
                translated.append(translate('apply_fungicide', language))
            elif 'spacing' in remedy_lower or 'circulation' in remedy_lower:
                translated.append(translate('proper_spacing', language))
            else:
                # Keep original if no translation available
                translated.append(remedy)
        
        return translated
    
    @staticmethod
    def _translate_fertilizers(fertilizers: List[str], language: str = 'en') -> List[str]:
        """Translate fertilizer recommendations"""
        if language == 'en':
            return fertilizers
        
        translated = []
        for fertilizer in fertilizers:
            # Try to match with known translation keys
            fert_lower = fertilizer.lower()
            if 'balanced npk' in fert_lower and '19:19:19' in fert_lower:
                translated.append(translate('balanced_npk', language))
            elif 'organic compost' in fert_lower or 'vermicompost' in fert_lower:
                translated.append(translate('organic_compost', language))
            elif 'micronutrient spray' in fert_lower:
                translated.append(translate('micronutrient_spray', language))
            elif 'potassium' in fert_lower:
                translated.append(translate('potassium_fertilizer', language))
            elif 'zinc' in fert_lower and 'manganese' in fert_lower:
                translated.append(translate('zinc_manganese', language))
            else:
                # Keep original if no translation available
                translated.append(fertilizer)
        
        return translated
    
    @staticmethod
    def _translate_prevention(prevention_tips: List[str], language: str = 'en') -> List[str]:
        """Translate prevention tips"""
        if language == 'en':
            return prevention_tips
        
        translated = []
        for tip in prevention_tips:
            # Try to match with known translation keys
            tip_lower = tip.lower()
            if 'avoid overhead watering' in tip_lower or 'drip irrigation' in tip_lower:
                translated.append(translate('avoid_overhead_watering', language))
            elif 'water' in tip_lower and 'morning' in tip_lower:
                translated.append(translate('water_morning', language))
            elif 'spacing' in tip_lower:
                translated.append(translate('maintain_spacing', language))
            elif 'debris' in tip_lower or 'weed' in tip_lower:
                translated.append(translate('remove_debris', language))
            elif 'mulch' in tip_lower:
                translated.append(translate('apply_mulch', language))
            elif 'monitor' in tip_lower:
                translated.append(translate('monitor_regularly', language))
            elif 'watering schedule' in tip_lower:
                translated.append(translate('proper_watering', language))
            elif 'air circulation' in tip_lower:
                translated.append(translate('ensure_circulation', language))
            elif 'damaged' in tip_lower or 'yellowing' in tip_lower:
                translated.append(translate('remove_damaged', language))
            elif 'clean' in tip_lower:
                translated.append(translate('keep_clean', language))
            else:
                # Keep original if no translation available
                translated.append(tip)
        
        return translated
