"""
Enhanced Disease Knowledge Base
Provides comprehensive, professional recommendations for farmers
"""

# Comprehensive disease database with detailed recommendations
DISEASE_KNOWLEDGE_BASE = {
    "Healthy": {
        "severity": "Excellent Health",
        "severity_level": "none",
        "confidence_note": "Your crop appears to be in excellent condition based on leaf color, texture, and structure analysis.",
        "analysis_details": [
            "✓ Leaf color is vibrant and uniform",
            "✓ No visible spots, lesions, or discoloration detected",
            "✓ Leaf structure appears healthy and well-formed",
            "✓ No signs of pest damage or disease patterns"
        ],
        "immediate_actions": [],
        "treatments": [],
        "fertilizer_recommendations": [
            {
                "product": "Balanced NPK Fertilizer (19:19:19)",
                "dosage": "Apply 2-3 grams per liter of water",
                "timing": "Every 15 days during growing season",
                "purpose": "Maintain overall plant health and vigor"
            },
            {
                "product": "Micronutrient Spray (Zinc, Iron, Manganese)",
                "dosage": "As per manufacturer instructions",
                "timing": "Once every 30 days",
                "purpose": "Prevent nutrient deficiencies"
            },
            {
                "product": "Organic Compost or Vermicompost",
                "dosage": "100-150 grams per plant",
                "timing": "Monthly application",
                "purpose": "Improve soil health and beneficial microorganisms"
            }
        ],
        "preventive_care": [
            " Continue current watering schedule - maintain consistent soil moisture",
            " Inspect plants every 3-4 days for early disease detection",
            " Remove any yellowing or damaged leaves promptly",
            " Ensure proper spacing (18-24 inches) for good air circulation",
            " Water at soil level in the morning to allow leaves to dry during the day",
            " Keep the growing area clean - remove weeds and plant debris weekly",
            " Monitor weather conditions - apply preventive fungicide before rainy season",
            " Check undersides of leaves for early pest detection"
        ],
        "what_not_to_do": [
            " Don't overwater - soggy soil promotes fungal diseases",
            " Avoid overhead watering in the evening (leaves stay wet overnight)",
            " Don't over-fertilize with nitrogen - makes plants susceptible to disease",
            " Never use contaminated tools without sterilization",
            " Don't ignore small symptoms - early detection is crucial",
            " Avoid planting in poorly drained areas"
        ],
        "monitoring_schedule": {
            "next_check": "3-4 days",
            "what_to_watch": [
                "Any yellowing or brown spots on leaves",
                "Changes in leaf color or texture",
                "Wilting despite adequate watering",
                "Presence of insects or pest damage",
                "White powdery coating (powdery mildew)",
                "Unusual leaf curling or deformation"
            ]
        },
        "expert_tip": "Your crop is healthy! Maintain current practices. Apply preventive measures before rainy season to avoid fungal diseases. Regular monitoring is key to catching problems early."
    },
    
    "Tomato Late Blight": {
        "severity": "Critical",
        "severity_level": "high",
        "confidence_note": "Late blight detected based on characteristic dark lesions on leaves. This is a serious fungal disease requiring immediate action.",
        "analysis_details": [
            " Dark water-soaked lesions detected on leaf surface",
            " Pattern consistent with Phytophthora infestans infection",
            " Risk of rapid spread to other plants is HIGH",
            " Can destroy entire crop within 7-10 days if untreated"
        ],
        "immediate_actions": [
            " URGENT: Remove and burn ALL infected leaves and plants immediately",
            " Isolate healthy plants from infected area",
            " Apply fungicide treatment within 24 hours",
            " Do NOT compost infected plant material - it will spread disease"
        ],
        "treatments": [
            {
                "step": 1,
                "product": "Metalaxyl + Mancozeb (Ridomil Gold)",
                "dosage": "2.5 grams per liter of water",
                "timing": "Spray immediately, repeat after 7 days",
                "application": "Thoroughly spray both sides of leaves until dripping",
                "cost_estimate": "₹200-300 per acre"
            },
            {
                "step": 2,
                "product": "Copper Oxychloride 50% WP",
                "dosage": "3 grams per liter of water",
                "timing": "14 days after first treatment",
                "application": "Spray in early morning or late evening",
                "cost_estimate": "₹150-200 per acre"
            },
            {
                "step": 3,
                "product": "Bordeaux Mixture (1%)",
                "dosage": "10 grams per liter (organic option)",
                "timing": "Every 10 days as preventive",
                "application": "Use as barrier spray on uninfected plants",
                "cost_estimate": "₹100-150 per acre"
            }
        ],
        "fertilizer_recommendations": [
            {
                "product": "Calcium Nitrate",
                "dosage": "2 grams per liter",
                "timing": "During treatment period",
                "purpose": "Strengthen cell walls, improve disease resistance"
            },
            {
                "product": "NPK 12:32:16",
                "dosage": "3 grams per liter",
                "timing": "After disease control",
                "purpose": "Help plant recover and strengthen stems"
            }
        ],
        "preventive_care": [
            " Improve air circulation - stake plants, prune lower branches",
            " Switch to drip irrigation immediately - NO overhead watering",
            " Monitor humidity levels - late blight thrives in humid conditions (>80%)",
            " Practice crop rotation - don't plant tomatoes in same spot for 3 years",
            " Use resistant varieties in next season (examples: Mountain Magic, Defiant PhR)",
            " Remove ALL crop debris after harvest and burn it",
            " Store harvested fruits away from infected areas"
        ],
        "what_not_to_do": [
            " NEVER water plants from above - this spreads spores rapidly",
            " Don't work with plants when they're wet (spreads disease)",
            " Never save seeds from infected plants",
            " Don't delay treatment - this disease spreads exponentially",
            " Avoid high nitrogen fertilizers during infection",
            " Don't plant potatoes nearby (same disease affects both)"
        ],
        "monitoring_schedule": {
            "next_check": "Daily for next 14 days",
            "what_to_watch": [
                "New lesions appearing on other plants",
                "White fuzzy growth on underside of leaves (sign of active spores)",
                "Stem lesions (disease has progressed)",
                "Fruit infection (brown rot with rings)",
                "Weather forecast - apply preventive spray before rain"
            ]
        },
        "expert_tip": "Late blight is the same disease that caused Irish Potato Famine. Act FAST! Remove infected plants, apply fungicide immediately, and improve air circulation. Consider this a crop emergency."
    },
    
    "Tomato Early Blight": {
        "severity": "Moderate",
        "severity_level": "moderate",
        "confidence_note": "Early blight detected based on characteristic concentric ring pattern on older leaves.",
        "analysis_details": [
            " Dark brown spots with concentric rings (bull's eye pattern) detected",
            " Pattern consistent with Alternaria solani fungal infection",
            " Typically starts on older lower leaves",
            " Can reduce yield by 20-30% if left untreated"
        ],
        "immediate_actions": [
            " Remove ALL affected lower leaves immediately",
            " Dispose of infected leaves away from garden (burn or deep bury)",
            " Apply fungicide treatment within 48 hours",
            " Inspect neighboring plants for early symptoms"
        ],
        "treatments": [
            {
                "step": 1,
                "product": "Chlorothalonil 75% WP (Kavach)",
                "dosage": "2 grams per liter of water",
                "timing": "Spray immediately, repeat every 7-10 days",
                "application": "Spray thoroughly covering lower leaves",
                "cost_estimate": "₹180-250 per acre"
            },
            {
                "step": 2,
                "product": "Mancozeb 75% WP (Dithane M-45)",
                "dosage": "2.5 grams per liter",
                "timing": "Alternate with Chlorothalonil every 7 days",
                "application": "Apply in early morning for better coverage",
                "cost_estimate": "₹150-200 per acre"
            },
            {
                "step": 3,
                "product": "Neem Oil (Organic option)",
                "dosage": "5 ml per liter + 1ml liquid soap",
                "timing": "Weekly spray for light infections",
                "application": "Spray in evening to avoid leaf burn",
                "cost_estimate": "₹100-150 per acre"
            }
        ],
        "fertilizer_recommendations": [
            {
                "product": "Balanced NPK 15:15:15",
                "dosage": "2 grams per liter",
                "timing": "Weekly during treatment",
                "purpose": "Maintain plant vigor during stress"
            },
            {
                "product": "Potassium Sulfate",
                "dosage": "1.5 grams per liter",
                "timing": "Every 10 days",
                "purpose": "Increase disease resistance"
            }
        ],
        "preventive_care": [
            " Apply organic mulch (straw, dried leaves) around plants - prevents soil splash",
            " Use drip irrigation or soaker hoses - keep leaves dry",
            " Prune lower branches for better air circulation (6 inches above soil)",
            " Ensure 24-30 inch spacing between plants",
            " Rotate crops - don't plant tomatoes in same spot for 2-3 years",
            " Clean up fallen leaves and plant debris weekly",
            " Apply preventive fungicide during humid weather"
        ],
        "what_not_to_do": [
            " Don't water leaves - only water at soil level",
            " Never work with wet plants (spreads spores)",
            " Don't over-fertilize with nitrogen (promotes disease)",
            " Avoid planting too close together",
            " Don't ignore early symptoms on lower leaves",
            " Never reuse stakes or cages without disinfection"
        ],
        "monitoring_schedule": {
            "next_check": "Every 3-4 days",
            "what_to_watch": [
                "New spots appearing on upper leaves",
                "Stem lesions (dark sunken areas)",
                "Spots on fruits (less common but serious)",
                "Rapid yellowing of leaves",
                "Check after rain or heavy dew"
            ]
        },
        "expert_tip": "Early blight is manageable if caught early. Remove infected leaves, apply fungicide, and most importantly - keep leaves DRY. Mulching prevents soil splash which spreads spores."
    },
    
    "Powdery Mildew": {
        "severity": "Moderate",
        "severity_level": "moderate",
        "confidence_note": "Powdery mildew detected based on white powdery coating on leaf surfaces.",
        "analysis_details": [
            " White powdery fungal growth detected on leaves",
            " Pattern consistent with powdery mildew infection",
            " Typically starts on upper leaf surfaces",
            " Thrives in moderate temperatures with high humidity"
        ],
        "immediate_actions": [
            " Remove severely infected leaves immediately",
            " Apply sulfur-based fungicide within 24-48 hours",
            " Improve air circulation around plants",
            " Increase sun exposure if possible"
        ],
        "treatments": [
            {
                "step": 1,
                "product": "Sulfur 80% WP (Sulphex)",
                "dosage": "3 grams per liter of water",
                "timing": "Spray immediately, repeat every 7 days",
                "application": "Spray in evening when temperature is below 32°C",
                "cost_estimate": "₹120-180 per acre"
            },
            {
                "step": 2,
                "product": "Potassium Bicarbonate Solution",
                "dosage": "5 grams per liter + 2ml liquid soap",
                "timing": "Weekly spray (organic option)",
                "application": "Spray both sides of leaves thoroughly",
                "cost_estimate": "₹80-120 per acre"
            },
            {
                "step": 3,
                "product": "Hexaconazole 5% SC",
                "dosage": "2 ml per liter",
                "timing": "For severe infections",
                "application": "Apply every 14 days, max 2-3 times per season",
                "cost_estimate": "₹250-350 per acre"
            }
        ],
        "fertilizer_recommendations": [
            {
                "product": "NPK 15:15:15 (Balanced)",
                "dosage": "2 grams per liter",
                "timing": "Bi-weekly",
                "purpose": "Avoid high nitrogen which promotes disease"
            },
            {
                "product": "Silicon-based Fertilizer",
                "dosage": "As per manufacturer instructions",
                "timing": "Monthly application",
                "purpose": "Strengthens cell walls, improves disease resistance"
            }
        ],
        "preventive_care": [
            " Plant in full sun location (minimum 6-8 hours daily)",
            " Prune for better air circulation - remove crowded branches",
            " Water at soil level early morning - never on leaves",
            " Avoid overcrowding - maintain 24-30 inch spacing",
            " Remove infected leaves and plant debris regularly",
            " Apply preventive sulfur spray bi-weekly during humid season",
            " Rotate crops yearly"
        ],
        "what_not_to_do": [
            " Don't apply sulfur when temperature exceeds 32°C (causes leaf burn)",
            " Never overhead water or water in evening",
            " Don't apply high nitrogen fertilizers",
            " Avoid dense planting",
            " Don't ignore early white spots",
            " Never spray in full sun (causes phytotoxicity)"
        ],
        "monitoring_schedule": {
            "next_check": "Every 2-3 days during treatment",
            "what_to_watch": [
                "White powder spreading to new leaves",
                "Yellowing and curling of infected leaves",
                "Stunted growth of young shoots",
                "Fruit surface infection (less common)",
                "Weather conditions - disease worsens in moderate temps with high humidity"
            ]
        },
        "expert_tip": "Powdery mildew is surface fungus - easier to control than deep infections. Sulfur spray works well. Key is improving air circulation and keeping leaves dry."
    },
    
    "Bacterial Spot": {
        "severity": "High",
        "severity_level": "high",
        "confidence_note": "Bacterial spot detected based on small dark lesions with yellow halos on leaves.",
        "analysis_details": [
            " Small dark brown spots with yellow halos detected",
            " Pattern consistent with Xanthomonas bacterial infection",
            " Can spread rapidly in warm, wet conditions",
            " May cause significant fruit damage and yield loss"
        ],
        "immediate_actions": [
            " Remove and destroy ALL infected plant parts immediately",
            " Apply copper-based bactericide within 24 hours",
            " Disinfect all tools with 10% bleach solution",
            " Avoid working with plants when wet"
        ],
        "treatments": [
            {
                "step": 1,
                "product": "Copper Oxychloride 50% WP + Streptocycline",
                "dosage": "3 grams COC + 0.5 gram Streptocycline per liter",
                "timing": "Spray immediately, repeat after 7 days",
                "application": "Thorough coverage including undersides of leaves",
                "cost_estimate": "₹200-300 per acre"
            },
            {
                "step": 2,
                "product": "Copper Hydroxide 77% WP",
                "dosage": "2.5 grams per liter",
                "timing": "Weekly spray during infection period",
                "application": "Apply in early morning",
                "cost_estimate": "₹180-250 per acre"
            },
            {
                "step": 3,
                "product": "Pseudomonas fluorescens (Bio-control)",
                "dosage": "10 grams per liter",
                "timing": "Weekly spray as supplementary treatment",
                "application": "Apply in evening for better bacterial survival",
                "cost_estimate": "₹150-200 per acre"
            }
        ],
        "fertilizer_recommendations": [
            {
                "product": "Calcium Nitrate",
                "dosage": "2-3 grams per liter",
                "timing": "Weekly during treatment",
                "purpose": "Strengthen cell walls against bacterial penetration"
            },
            {
                "product": "NPK 12:32:16",
                "dosage": "2 grams per liter",
                "timing": "Bi-weekly",
                "purpose": "Maintain plant vigor during stress"
            }
        ],
        "preventive_care": [
            " Use certified disease-free seeds and transplants",
            " Sterilize all tools, stakes, and cages between uses (10% bleach)",
            " Use drip irrigation - NEVER overhead watering",
            " Increase plant spacing to 30-36 inches",
            " Rotate with non-solanaceous crops for 2-3 years",
            " Avoid working when plants are wet from dew or rain",
            " Control leaf-feeding insects that create entry points",
            " Source transplants from reputable nurseries only"
        ],
        "what_not_to_do": [
            " NEVER save seeds from infected plants",
            " Don't touch plants when wet (spreads bacteria)",
            " Never use contaminated tools without sterilization",
            " Don't overhead water or handle during rain",
            " Avoid high nitrogen fertilization",
            " Never compost infected plant material"
        ],
        "monitoring_schedule": {
            "next_check": "Daily for next 10 days",
            "what_to_watch": [
                "New spots appearing on young leaves",
                "Fruit lesions (raised scabby spots)",
                "Rapid yellowing and defoliation",
                "Stem cankers (dark streaks)",
                "Weather - disease spreads rapidly in warm rain"
            ]
        },
        "expert_tip": "Bacterial diseases have NO CURE - only management. Prevention is crucial! Use copper sprays, practice strict sanitation, and never work with wet plants. Source disease-free seedlings."
    }
}

def get_disease_info(disease_name):
    """
    Get comprehensive disease information with flexible matching
    Handles exact match and partial matching for disease names
    """
    # Try exact match first
    if disease_name in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[disease_name]
    
    # Try case-insensitive exact match
    for key in DISEASE_KNOWLEDGE_BASE:
        if key.lower() == disease_name.lower():
            return DISEASE_KNOWLEDGE_BASE[key]
    
    # Try partial match - check if any key contains the disease name
    disease_lower = disease_name.lower()
    for key in DISEASE_KNOWLEDGE_BASE:
        key_lower = key.lower()
        # Check if disease name contains the key or key contains disease name
        if 'late blight' in disease_lower and 'late blight' in key_lower:
            return DISEASE_KNOWLEDGE_BASE[key]
        elif 'early blight' in disease_lower and 'early blight' in key_lower:
            return DISEASE_KNOWLEDGE_BASE[key]
        elif 'powdery mildew' in disease_lower and 'powdery mildew' in key_lower:
            return DISEASE_KNOWLEDGE_BASE[key]
        elif 'bacterial spot' in disease_lower and 'bacterial spot' in key_lower:
            return DISEASE_KNOWLEDGE_BASE[key]
    
    # Default to healthy if no match found
    return DISEASE_KNOWLEDGE_BASE["Healthy"]
