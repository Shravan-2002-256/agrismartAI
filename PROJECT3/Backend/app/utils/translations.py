"""
Translation utilities for AgriSmart AI
Provides translations for dynamic backend content
"""

TRANSLATIONS = {
    'en': {
        # Crop names
        'tomato': 'Tomato',
        'potato': 'Potato',
        'corn': 'Corn',
        'wheat': 'Wheat',
        'rice': 'Rice',
        'grape': 'Grape',
        'apple': 'Apple',
        'pepper': 'Pepper',
        'strawberry': 'Strawberry',
        'peach': 'Peach',
        'orange': 'Orange',
        'soybean': 'Soybean',
        'cherry': 'Cherry',
        
        # Disease names
        'healthy': 'Healthy',
        'healthy_plants': 'Healthy Plants',
        'leaf_spot': 'Leaf Spot Disease',
        'tomato_late_blight': 'Tomato Late Blight',
        'tomato_early_blight': 'Tomato Early Blight',
        'powdery_mildew': 'Powdery Mildew',
        'bacterial_spot': 'Bacterial Spot',
        'blight': 'Blight',
        
        # Health status messages
        'health_status_low': 'Great news! Your crops are healthy. Only {percent}% show minor issues. Continue current practices.',
        'health_status_moderate': 'Moderate disease activity in your crops. {percent}% of images show symptoms across {crop_count} crop types. Follow recommendations to control spread.',
        'health_status_high': 'High disease pressure detected! {percent}% of your crops show significant disease symptoms. Immediate action required.',
        'health_status_critical': 'Critical alert! {percent}% of crops are severely affected. Take emergency measures immediately.',
        
        # Crop insights messages
        'healthy_message': 'Great news! {percent}% of your {crop} plants ({healthy} out of {total}) are healthy and thriving. Continue with current care practices.',
        'critical_alert': '⚠️ Critical Alert: {percent}% of your {crop} images ({diseased} out of {total}) show signs of {disease}. This is a widespread pattern requiring immediate attention.',
        
        # Action status
        'keep_monitoring': 'Keep monitoring',
        'action_needed_soon': 'Action needed soon',
        'immediate_action_required': 'Immediate action required',
        
        # Treatment & Care
        'continue_monitoring': 'Continue regular monitoring',
        'maintain_practices': 'Maintain current care practices',
        'remove_affected': 'Remove and destroy affected leaves immediately',
        'apply_fungicide': 'Apply copper-based fungicide',
        'proper_spacing': 'Ensure proper spacing between plants for air circulation',
        'avoid_overhead_watering': 'Avoid overhead watering - use drip irrigation',
        'water_morning': 'Water in the morning to allow leaves to dry',
        'maintain_spacing': 'Maintain proper plant spacing',
        'remove_debris': 'Remove crop debris and weeds regularly',
        'apply_mulch': 'Apply organic mulch to prevent soil splash',
        'monitor_regularly': 'Monitor plants regularly for early disease detection',
        'proper_watering': 'Maintain proper watering schedule',
        'ensure_circulation': 'Ensure adequate spacing and air circulation',
        'remove_damaged': 'Remove any yellowing or damaged leaves',
        'keep_clean': 'Keep growing area clean and weed-free',
        
        # Fertilizer recommendations
        'balanced_npk': 'Apply balanced NPK 19:19:19 @ 2g/liter every 15 days',
        'organic_compost': 'Use organic compost or vermicompost @ 100g/plant monthly',
        'micronutrient_spray': 'Apply micronutrient spray once a month',
        'potassium_fertilizer': 'Add potassium fertilizer to strengthen plant immunity',
        'zinc_manganese': 'Use micronutrient spray with Zinc and Manganese',
    },
    
    'te': {
        # Crop names (Telugu)
        'tomato': 'టమోటా',
        'potato': 'బంగాళాదుంప',
        'corn': 'మొక్కజొన్న',
        'wheat': 'గోధుమ',
        'rice': 'వరి',
        'grape': 'ద్రాక్ష',
        'apple': 'యాపిల్',
        'pepper': 'మిరపకాయ',
        'strawberry': 'స్ట్రాబెర్రీ',
        'peach': 'పీచు',
        'orange': 'నారింజ',
        'soybean': 'సోయాబీన్',
        'cherry': 'చెర్రీ',
        
        # Disease names (Telugu)
        'healthy': 'ఆరోగ్యకరమైన',
        'healthy_plants': 'ఆరోగ్యకరమైన మొక్కలు',
        'leaf_spot': 'ఆకు మచ్చ వ్యాధి',
        'tomato_late_blight': 'టమోటా లేట్ బ్లైట్',
        'tomato_early_blight': 'టమోటా ఎర్లీ బ్లైట్',
        'powdery_mildew': 'పౌడర్ మిల్డ్యూ',
        'bacterial_spot': 'బ్యాక్టీరియల్ స్పాట్',
        'blight': 'బ్లైట్',
        
        # Health status messages (Telugu)
        'health_status_low': 'గొప్ప వార్త! మీ పంటలు ఆరోగ్యంగా ఉన్నాయి. కేవలం {percent}% చిన్న సమస్యలను చూపిస్తున్నాయి. ప్రస్తుత పద్ధతులను కొనసాగించండి.',
        'health_status_moderate': 'మీ పంటలలో మితమైన వ్యాధి కార్యకలాపాలు. {crop_count} పంట రకాల్లో {percent}% చిత్రాలు లక్షణాలను చూపిస్తున్నాయి. వ్యాప్తిని నియంత్రించడానికి సిఫార్సులను అనుసరించండి.',
        'health_status_high': 'అధిక వ్యాధి ఒత్తిడి కనుగొనబడింది! మీ పంటలలో {percent}% గణనీయమైన వ్యాధి లక్షణాలను చూపుతున్నాయి. తక్షణ చర్య అవసరం.',
        'health_status_critical': 'క్లిష్టమైన హెచ్చరిక! పంటలలో {percent}% తీవ్రంగా ప్రభావితమై ఉన్నాయి. తక్షణం అత్యవసర చర్యలు తీసుకోండి.',
        
        # Crop insights messages (Telugu)
        'healthy_message': 'గొప్ప వార్త! మీ {crop} మొక్కలలో {percent}% ({total}లో {healthy}) ఆరోగ్యంగా మరియు బాగా పెరుగుతున్నాయి. ప్రస్తుత సంరక్షణ పద్ధతులను కొనసాగించండి.',
        'critical_alert': '⚠️ క్లిష్టమైన హెచ్చరిక: మీ {crop} చిత్రాలలో {percent}% ({total}లో {diseased}) {disease} సంకేతాలను చూపిస్తున్నాయి. ఇది తక్షణ శ్రద్ధ అవసరమైన విస్తృత నమూనా.',
        
        # Action status (Telugu)
        'keep_monitoring': 'పర్యవేక్షణ కొనసాగించండి',
        'action_needed_soon': 'త్వరలో చర్య అవసరం',
        'immediate_action_required': 'తక్షణ చర్య అవసరం',
        
        # Treatment & Care (Telugu)
        'continue_monitoring': 'నిరంతర పర్యవేక్షణ కొనసాగించండి',
        'maintain_practices': 'ప్రస్తుత సంరక్షణ పద్ధతులను కొనసాగించండి',
        'remove_affected': 'ప్రభావిత ఆకులను వెంటనే తొలగించి నాశనం చేయండి',
        'apply_fungicide': 'కాపర్-ఆధారిత శిలీంద్రనాశిని వర్తించండి',
        'proper_spacing': 'గాలి ప్రసరణ కోసం మొక్కల మధ్య సరైన దూరం నిర్ధారించండి',
        'avoid_overhead_watering': 'పై నుండి నీటిపారుదలను నివారించండి - డ్రిప్ నీటిపారుదల ఉపయోగించండి',
        'water_morning': 'ఆకులు ఆరిపోవడానికి ఉదయం నీటిపారుదల చేయండి',
        'maintain_spacing': 'సరైన మొక్కల దూరం నిర్వహించండి',
        'remove_debris': 'పంట శిథిలాలు మరియు కలుపు మొక్కలను క్రమం తప్పకుండా తొలగించండి',
        'apply_mulch': 'మట్టి చిమ్ముడును నివారించడానికి సేంద్రీయ మల్చ్ వర్తించండి',
        'monitor_regularly': 'ప్రారంభ వ్యాధి గుర్తింపు కోసం మొక్కలను క్రమం తప్పకుండా పర్యవేక్షించండి',
        'proper_watering': 'సరైన నీటిపారుదల షెడ్యూల్ నిర్వహించండి',
        'ensure_circulation': 'తగినంత దూరం మరియు గాలి ప్రసరణను నిర్ధారించండి',
        'remove_damaged': 'ఏదైనా పసుపు లేదా దెబ్బతిన్న ఆకులను తొలగించండి',
        'keep_clean': 'పెరుగుతున్న ప్రాంతాన్ని శుభ్రంగా మరియు కలుపు లేకుండా ఉంచండి',
        
        # Fertilizer recommendations (Telugu)
        'balanced_npk': 'ప్రతి 15 రోజులకు సమతుల్య NPK 19:19:19 @ 2గ్రా/లీటర్ వర్తించండి',
        'organic_compost': 'సేంద్రీయ కంపోస్ట్ లేదా వర్మికంపోస్ట్ @ 100గ్రా/మొక్క నెలవారీగా ఉపయోగించండి',
        'micronutrient_spray': 'నెలకు ఒకసారి సూక్ష్మపోషక స్ప్రే వర్తించండి',
        'potassium_fertilizer': 'మొక్క రోగనిరోధక శక్తిని బలపరచడానికి పొటాషియం ఎరువు జోడించండి',
        'zinc_manganese': 'జింక్ మరియు మాంగనీస్‌తో సూక్ష్మపోషక స్ప్రే ఉపయోగించండి',
    },
    
    'hi': {
        # Crop names (Hindi)
        'tomato': 'टमाटर',
        'potato': 'आलू',
        'corn': 'मकई',
        'wheat': 'गेहूं',
        'rice': 'चावल',
        'grape': 'अंगूर',
        'apple': 'सेब',
        'pepper': 'मिर्च',
        'strawberry': 'स्ट्रॉबेरी',
        'peach': 'आड़ू',
        'orange': 'संतरा',
        'soybean': 'सोयाबीन',
        'cherry': 'चेरी',
        
        # Disease names (Hindi)
        'healthy': 'स्वस्थ',
        'healthy_plants': 'स्वस्थ पौधे',
        'leaf_spot': 'पत्ती धब्बा रोग',
        'tomato_late_blight': 'टमाटर लेट ब्लाइट',
        'tomato_early_blight': 'टमाटर अर्ली ब्लाइट',
        'powdery_mildew': 'पाउडरी मिल्ड्यू',
        'bacterial_spot': 'बैक्टीरियल स्पॉट',
        'blight': 'ब्लाइट',
        
        # Health status messages (Hindi)
        'health_status_low': 'बढ़िया खबर! आपकी फसलें स्वस्थ हैं। केवल {percent}% मामूली समस्याएं दिखाती हैं। वर्तमान प्रथाओं को जारी रखें।',
        'health_status_moderate': 'आपकी फसलों में मध्यम रोग गतिविधि। {crop_count} फसल प्रकारों में {percent}% छवियां लक्षण दिखाती हैं। फैलाव को नियंत्रित करने के लिए सिफारिशों का पालन करें।',
        'health_status_high': 'उच्च रोग दबाव का पता चला! आपकी फसलों में {percent}% महत्वपूर्ण रोग के लक्षण दिखाती हैं। तत्काल कार्रवाई आवश्यक।',
        'health_status_critical': 'गंभीर चेतावनी! फसलों का {percent}% गंभीर रूप से प्रभावित है। तुरंत आपातकालीन उपाय करें।',
        
        # Crop insights messages (Hindi)
        'healthy_message': 'बढ़िया खबर! आपके {crop} पौधों का {percent}% ({total} में से {healthy}) स्वस्थ है और फल-फूल रहा है। वर्तमान देखभाल प्रथाओं को जारी रखें।',
        'critical_alert': '⚠️ महत्वपूर्ण चेतावनी: आपकी {crop} छवियों का {percent}% ({total} में से {diseased}) {disease} के संकेत दिखाता है। यह एक व्यापक पैटर्न है जिसमें तत्काल ध्यान देने की आवश्यकता है।',
        
        # Action status (Hindi)
        'keep_monitoring': 'निगरानी जारी रखें',
        'action_needed_soon': 'जल्द ही कार्रवाई की जरूरत',
        'immediate_action_required': 'तत्काल कार्रवाई आवश्यक',
        
        # Treatment & Care (Hindi)
        'continue_monitoring': 'नियमित निगरानी जारी रखें',
        'maintain_practices': 'वर्तमान देखभाल प्रथाओं को बनाए रखें',
        'remove_affected': 'प्रभावित पत्तियों को तुरंत हटाएं और नष्ट करें',
        'apply_fungicide': 'तांबा-आधारित फफूंदनाशक लागू करें',
        'proper_spacing': 'वायु संचार के लिए पौधों के बीच उचित दूरी सुनिश्चित करें',
        'avoid_overhead_watering': 'ऊपर से पानी देने से बचें - ड्रिप सिंचाई का उपयोग करें',
        'water_morning': 'पत्तियों को सूखने देने के लिए सुबह पानी दें',
        'maintain_spacing': 'उचित पौधे की दूरी बनाए रखें',
        'remove_debris': 'फसल के मलबे और खरपतवार को नियमित रूप से हटाएं',
        'apply_mulch': 'मिट्टी के छींटे को रोकने के लिए जैविक गीली घास लगाएं',
        'monitor_regularly': 'प्रारंभिक रोग का पता लगाने के लिए पौधों की नियमित रूप से निगरानी करें',
        'proper_watering': 'उचित पानी देने का कार्यक्रम बनाए रखें',
        'ensure_circulation': 'पर्याप्त दूरी और वायु संचार सुनिश्चित करें',
        'remove_damaged': 'कोई भी पीली या क्षतिग्रस्त पत्तियां हटा दें',
        'keep_clean': 'बढ़ते क्षेत्र को साफ और खरपतवार मुक्त रखें',
        
        # Fertilizer recommendations (Hindi)
        'balanced_npk': 'हर 15 दिन में संतुलित NPK 19:19:19 @ 2ग्राम/लीटर लगाएं',
        'organic_compost': 'जैविक खाद या वर्मीकम्पोस्ट @ 100ग्राम/पौधा मासिक उपयोग करें',
        'micronutrient_spray': 'महीने में एक बार सूक्ष्म पोषक तत्व स्प्रे लगाएं',
        'potassium_fertilizer': 'पौधे की प्रतिरक्षा को मजबूत करने के लिए पोटेशियम उर्वरक जोड़ें',
        'zinc_manganese': 'जिंक और मैंगनीज के साथ सूक्ष्म पोषक तत्व स्प्रे का उपयोग करें',
    },
    
    'ta': {
        # Crop names (Tamil)
        'tomato': 'தக்காளி',
        'potato': 'உருளைக்கிழங்கு',
        'corn': 'சோளம்',
        'wheat': 'கோதுமை',
        'rice': 'அரிசி',
        'grape': 'திராட்சை',
        'apple': 'ஆப்பிள்',
        'pepper': 'மிளகாய்',
        'strawberry': 'ஸ்ட்ராபெர்ரி',
        'peach': 'பீச்',
        'orange': 'ஆரஞ்சு',
        'soybean': 'சோயாபீன்',
        'cherry': 'செர்ரி',
        
        # Disease names (Tamil)
        'healthy': 'ஆரோக்கியமான',
        'healthy_plants': 'ஆரோக்கியமான செடிகள்',
        'leaf_spot': 'இலை புள்ளி நோய்',
        'tomato_late_blight': 'தக்காளி லேட் பிளைட்',
        'tomato_early_blight': 'தக்காளி எர்லி பிளைட்',
        'powdery_mildew': 'பௌடரி மில்ட்யூ',
        'bacterial_spot': 'பாக்டீரியல் ஸ்பாட்',
        'blight': 'பிளைட்',
        
        # Health status messages (Tamil)
        'health_status_low': 'நல்ல செய்தி! உங்கள் பயிர்கள் ஆரோக்கியமாக உள்ளன. {percent}% மட்டுமே சிறிய பிரச்சினைகளைக் காட்டுகின்றன. தற்போதைய நடைமுறைகளைத் தொடரவும்.',
        'health_status_moderate': 'உங்கள் பயிர்களில் மிதமான நோய் செயல்பாடு. {crop_count} பயிர் வகைகளில் {percent}% படங்கள் அறிகுறிகளைக் காட்டுகின்றன. பரவலைக் கட்டுப்படுத்த பரிந்துரைகளைப் பின்பற்றவும்.',
        'health_status_high': 'அதிக நோய் அழுத்தம் கண்டறியப்பட்டது! உங்கள் பயிர்களில் {percent}% குறிப்பிடத்தக்க நோய் அறிகுறிகளைக் காட்டுகிறது. உடனடி நடவடிக்கை தேவை.',
        'health_status_critical': 'முக்கியமான எச்சரிக்கை! பயிர்களில் {percent}% கடுமையாக பாதிக்கப்பட்டுள்ளது. உடனடியாக அவசர நடவடிக்கைகளை எடுக்கவும்.',
        
        # Crop insights messages (Tamil)
        'healthy_message': 'நல்ல செய்தி! உங்கள் {crop} செடிகளில் {percent}% ({total} இல் {healthy}) ஆரோக்கியமாகவும் செழிப்பாகவும் உள்ளன. தற்போதைய பராமரிப்பு முறைகளைத் தொடரவும்.',
        'critical_alert': '⚠️ முக்கியமான எச்சரிக்கை: உங்கள் {crop} படங்களில் {percent}% ({total} இல் {diseased}) {disease} அறிகுறிகளைக் காட்டுகின்றன. இது உடனடி கவனம் தேவைப்படும் பரவலான வடிவமாகும்.',
        
        # Action status (Tamil)
        'keep_monitoring': 'கண்காணிப்பைத் தொடரவும்',
        'action_needed_soon': 'விரைவில் நடவடிக்கை தேவை',
        'immediate_action_required': 'உடனடி நடவடிக்கை தேவை',
        
        # Treatment & Care (Tamil)
        'continue_monitoring': 'தொடர்ந்து கண்காணிப்பைத் தொடரவும்',
        'maintain_practices': 'தற்போதைய பராமரிப்பு முறைகளை பராமரிக்கவும்',
        'remove_affected': 'பாதிக்கப்பட்ட இலைகளை உடனடியாக அகற்றி அழிக்கவும்',
        'apply_fungicide': 'செம்பு அடிப்படையிலான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்',
        'proper_spacing': 'காற்று சுழற்சிக்கு செடிகளுக்கு இடையே சரியான இடைவெளியை உறுதி செய்யவும்',
        'avoid_overhead_watering': 'மேலே நீர் பாய்ச்சுதலை தவிர்க்கவும் - சொட்டு நீர் பாய்ச்சலைப் பயன்படுத்தவும்',
        'water_morning': 'இலைகள் காய அனுமதிக்க காலையில் தண்ணீர் பாய்ச்சவும்',
        'maintain_spacing': 'சரியான செடி இடைவெளியை பராமரிக்கவும்',
        'remove_debris': 'பயிர் குப்பைகள் மற்றும் களைகளை தொடர்ந்து அகற்றவும்',
        'apply_mulch': 'மண் தெறிப்பதைத் தடுக்க கரிம மல்ச் பயன்படுத்தவும்',
        'monitor_regularly': 'ஆரம்ப நோய் கண்டறிதலுக்கு செடிகளை தொடர்ந்து கண்காணிக்கவும்',
        'proper_watering': 'சரியான நீர்ப்பாசன அட்டவணையை பராமரிக்கவும்',
        'ensure_circulation': 'போதுமான இடைவெளி மற்றும் காற்று சுழற்சியை உறுதி செய்யவும்',
        'remove_damaged': 'ஏதேனும் மஞ்சள் அல்லது சேதமடைந்த இலைகளை அகற்றவும்',
        'keep_clean': 'வளரும் பகுதியை சுத்தமாகவும் களை இல்லாததாகவும் வைக்கவும்',
        
        # Fertilizer recommendations (Tamil)
        'balanced_npk': 'ஒவ்வொரு 15 நாட்களுக்கும் சமதூக்கு NPK 19:19:19 @ 2கி/லிட்டர் பயன்படுத்தவும்',
        'organic_compost': 'கரிம உரம் அல்லது வெர்மி உரம் @ 100கி/செடி மாதாந்திரம் பயன்படுத்தவும்',
        'micronutrient_spray': 'மாதம் ஒருமுறை நுண்ணூட்டச்சத்து தெளிப்பை பயன்படுத்தவும்',
        'potassium_fertilizer': 'செடி நோயெதிர்ப்பு சக்தியை வலுப்படுத்த பொட்டாசியம் உரத்தை சேர்க்கவும்',
        'zinc_manganese': 'துத்தநாகம் மற்றும் மாங்கனீசுடன் நுண்ணூட்டச்சத்து தெளிப்பைப் பயன்படுத்தவும்',
    }
}

def translate(key: str, language: str = 'en', **kwargs) -> str:
    """
    Translate a key to the specified language
    
    Args:
        key: Translation key
        language: Target language code (en, hi, te, ta)
        **kwargs: Format parameters for the translation string
        
    Returns:
        Translated string
    """
    lang_dict = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    translation = lang_dict.get(key, TRANSLATIONS['en'].get(key, key))
    
    # Format the string if kwargs provided
    if kwargs:
        try:
            translation = translation.format(**kwargs)
        except KeyError:
            pass
    
    return translation

def translate_crop_name(crop_name: str, language: str = 'en') -> str:
    """Translate crop name to specified language"""
    key = crop_name.lower().replace(' ', '_')
    return translate(key, language)

def translate_disease_name(disease_name: str, language: str = 'en') -> str:
    """Translate disease name to specified language"""
    # Map disease names to keys
    disease_map = {
        'Healthy': 'healthy',
        'Healthy Plants': 'healthy_plants',
        'Leaf Spot': 'leaf_spot',
        'Leaf Spot Disease': 'leaf_spot',
        'Tomato Late Blight': 'tomato_late_blight',
        'Tomato Early Blight': 'tomato_early_blight',
        'Powdery Mildew': 'powdery_mildew',
        'Bacterial Spot': 'bacterial_spot',
        'Blight': 'blight',
    }
    
    key = disease_map.get(disease_name, disease_name.lower().replace(' ', '_'))
    return translate(key, language)
