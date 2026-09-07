/**
 * iGOT Karmayogi Multilingual Translation Engine
 * Supports 10 major official languages of India
 * EN (English), HI (Hindi), BN (Bengali), TE (Telugu), TA (Tamil),
 * MR (Marathi), GU (Gujarati), KN (Kannada), ML (Malayalam), PA (Punjabi)
 */

const SUPPORTED_LANGUAGES = [
  { code: "en", name: "English", label: "English" },
  { code: "hi", name: "हिन्दी", label: "Hindi" },
  { code: "bn", name: "বাংলা", label: "Bengali" },
  { code: "te", name: "తెలుగు", label: "Telugu" },
  { code: "ta", name: "தமிழ்", label: "Tamil" },
  { code: "mr", name: "मराठी", label: "Marathi" },
  { code: "gu", name: "ગુજરાતી", label: "Gujarati" },
  { code: "kn", name: "ಕನ್ನಡ", label: "Kannada" },
  { code: "ml", name: "മലയാളം", label: "Malayalam" },
  { code: "pa", name: "ਪੰਜਾਬੀ", label: "Punjabi" }
];

const I18N_DICTIONARY = {
  // Navigation & Branding
  "iGOT Karmayogi": {
    hi: "आईगॉट कर्मयोगी",
    bn: "আইগট কর্মযোগী",
    te: "ఐగాట్ కర్మయోగి",
    ta: "ஐகாட் கர்மயோகி",
    mr: "आयगॉट कर्मयोगी",
    gu: "આઈગોટ કર્મયોગી",
    kn: "ಐಗಾಟ್ ಕರ್ಮಯೋಗಿ",
    ml: "ഐഗോട്ട് കർമ്മയോഗി",
    pa: "ਆਈਗੌਟ ਕਰਮਯੋਗੀ"
  },
  "कर्मण्योगी भारत": {
    hi: "कर्मयोगी भारत",
    bn: "কর্মযোগী ভারত",
    te: "కర్మయోగి భారత్",
    ta: "கர்மயோகி பாரத்",
    mr: "कर्मयोगी भारत",
    gu: "કર્મયોગી ભારત",
    kn: "ಕರ್ಮಯೋಗಿ ಭಾರತ",
    ml: "കർമ്മയോഗി ഭാരത്",
    pa: "ਕਰਮਯੋਗੀ ਭਾਰਤ"
  },
  "लोकलहित में कार्यतात्": {
    hi: "लोकलहित में कार्यतात्",
    bn: "জনস্বার্থে সেবারত",
    te: "ప్రజా సంక్షేమంలో సేవ",
    ta: "மக்கள் நலனில் சேவை",
    mr: "लोककल्याणार्थ कार्यतत्पर",
    gu: "લોકહિતમાં કાર્યરત",
    kn: "ಜನಹಿತದಲ್ಲಿ ಕರ್ತವ್ಯ",
    ml: "ജനക്ഷേമത്തിൽ സേവനനിരതം",
    pa: "ਲੋਕ ਹਿੱਤ ਵਿੱਚ ਕਾਰਜਸ਼ੀਲ"
  },
  "Dashboard": {
    hi: "डैशबोर्ड",
    bn: "ড্যাশবোর্ড",
    te: "డ్యాష్‌బోర్డ్",
    ta: "டாஷ்போர்டு",
    mr: "डॅशबोर्ड",
    gu: "ડેશબોર્ડ",
    kn: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    ml: "ഡാഷ്‌ബോർഡ്",
    pa: "ਡੈਸ਼ਬੋਰਡ"
  },
  "My Dashboard": {
    hi: "मेरा डैशबोर्ड",
    bn: "আমার ড্যাশবোর্ড",
    te: "నా డ్యాష్‌బోర్డ్",
    ta: "என் டாஷ்போர்டு",
    mr: "माझे डॅशबोर्ड",
    gu: "મારું ડેશબોર્ડ",
    kn: "ನನ್ನ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    ml: "എന്റെ ഡാഷ്‌ബോർഡ്",
    pa: "ਮੇਰਾ ਡੈਸ਼ਬੋਰਡ"
  },
  "Trainer Studio": {
    hi: "प्रशिक्षक स्टूडियो",
    bn: "প্রশিক্ষক স্টুডিও",
    te: "ట్రైనర్ స్టూడియో",
    ta: "பயிற்சியாளர் ஸ்டுடியோ",
    mr: "प्रशिक्षक स्टुडिओ",
    gu: "ટ્રેનર સ્ટુડિયો",
    kn: "ತರಬೇತುದಾರ ಸ್ಟುಡಿಯೋ",
    ml: "ട്രെയിനർ സ്റ്റുഡിയോ",
    pa: "ਟ੍ਰੇਨਰ ਸਟੂਡੀਓ"
  },
  "Analytics": {
    hi: "विश्लेषिकी",
    bn: "বিশ্লেষণ",
    te: "విశ్లేషణలు",
    ta: "பகுப்பாய்வு",
    mr: "विश्लेषण",
    gu: "વિશ્લેષણ",
    kn: "ವಿಶ್ಲೇಷಣೆ",
    ml: "വിശകലനം",
    pa: "ਵਿਸ਼ਲੇਸ਼ਣ"
  },
  "Organization Analytics": {
    hi: "संस्थागत विश्लेषिकी",
    bn: "প্রাতিষ্ঠানিক বিশ্লেষণ",
    te: "సంస్థ విశ్లేషణలు",
    ta: "நிறுவன பகுப்பாய்வு",
    mr: "संस्थागत विश्लेषण",
    gu: "સંસ્થાકીય વિશ્લેષણ",
    kn: "ಸಂಸ್ಥೆಯ ವಿಶ್ಲೇಷಣೆ",
    ml: "സ്ഥാപന വിശകലനം",
    pa: "ਸੰਸਥਾਗਤ ਵਿਸ਼ਲੇਸ਼ਣ"
  },
  "Home": {
    hi: "होम",
    bn: "হোম",
    te: "హోమ్",
    ta: "முகப்பு",
    mr: "मुख्यपृष्ठ",
    gu: "હોમ",
    kn: "ಮುಖಪುಟ",
    ml: "ഹോം",
    pa: "ਮੁੱਖ ਪੰਨਾ"
  },
  "Login": {
    hi: "लॉग इन",
    bn: "লগইন",
    te: "లాగిన్",
    ta: "உள்நுழைக",
    mr: "लॉग इन",
    gu: "લૉગ ઇન",
    kn: "ಲಾಗಿನ್",
    ml: "ലോഗിൻ",
    pa: "ਲਾਗਇਨ"
  },
  "Log in": {
    hi: "लॉग इन करें",
    bn: "লগইন করুন",
    te: "లాగిన్ చేయండి",
    ta: "உள்நுழைய",
    mr: "लॉग इन करा",
    gu: "લૉગ ઇન કરો",
    kn: "ಲಾಗಿನ್ ಮಾಡಿ",
    ml: "ലോഗിൻ ചെയ്യുക",
    pa: "ਲਾਗਇਨ ਕਰੋ"
  },
  "Register": {
    hi: "पंजीकरण",
    bn: "নিবন্ধন",
    te: "నమోదు",
    ta: "பதிவு செய்க",
    mr: "नोंदणी",
    gu: "નોંધણી",
    kn: "ನೋಂದಣಿ",
    ml: "രജിസ്റ്റർ ചെയ്യുക",
    pa: "ਰਜਿਸਟਰੇਸ਼ਨ"
  },
  "Log out": {
    hi: "लॉग आउट",
    bn: "লগ আউট",
    te: "లాగ్ అవుట్",
    ta: "வெளியேறு",
    mr: "लॉग आउट",
    gu: "લૉગ આઉટ",
    kn: "ಲಾಗ್ ಔಟ್",
    ml: "ലോഗ് ഔട്ട്",
    pa: "ਲਾਗ ਆਊਟ"
  },
  "Namaste": {
    hi: "नमस्ते",
    bn: "নমস্কার",
    te: "నమస్తే",
    ta: "வணக்கம்",
    mr: "नमस्ते",
    gu: "નમસ્તે",
    kn: "ನಮಸ್ಕಾರ",
    ml: "നമസ്കാരം",
    pa: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ"
  },
  "Administrator": {
    hi: "प्रशासक",
    bn: "প্রশাসক",
    te: "అడ్మినిస్ట్రేటర్",
    ta: "நிர்வாகி",
    mr: "प्रशासक",
    gu: "સંચાલક",
    kn: "ಆಡಳಿತಾಧಿಕಾರಿ",
    ml: "അഡ്മിനിസ്ട്രേറ്റർ",
    pa: "ਪ੍ਰਬੰਧਕ"
  },
  "Read-only": {
    hi: "केवल-पठन",
    bn: "কেবল-পাঠযোগ্য",
    te: "చదవడం మాత్రమే",
    ta: "படிக்க மட்டும்",
    mr: "फक्त वाचनीय",
    gu: "માત્ર વાંચન",
    kn: "ಓದಲು ಮಾತ್ರ",
    ml: "വായിക്കാൻ മാത്രം",
    pa: "ਸਿਰਫ਼ ਪੜ੍ਹਨਯੋਗ"
  },

  // Govt Strip & Footer
  "भारत सरकार · Government of India": {
    hi: "भारत सरकार · Government of India",
    bn: "ভারত সরকার · Government of India",
    te: "భారత ప్రభుత్వం · Government of India",
    ta: "இந்திய அரசு · Government of India",
    mr: "भारत सरकार · Government of India",
    gu: "ભારત સરકાર · Government of India",
    kn: "ಭಾರತ ಸರ್ಕಾರ · Government of India",
    ml: "ഭാരത സർക്കാർ · Government of India",
    pa: "ਭਾਰਤ ਸਰਕਾਰ · Government of India"
  },
  "Department of Personnel & Training · Mission Karmayogi": {
    hi: "कार्मिक एवं प्रशिक्षण विभाग · मिशन कर्मयोगी",
    bn: "কর্মী ও প্রশিক্ষণ বিভাগ · মিশন কর্মযোগী",
    te: "పర్సనల్ & ట్రైనింగ్ విభాగం · మిషన్ కర్మయోగి",
    ta: "பணியாளர் மற்றும் பயிற்சித் துறை · மிஷன் கர்மயோகி",
    mr: "कार्मिक व प्रशिक्षण विभाग · मिशन कर्मयोगी",
    gu: "કર્મચારી અને તાલીમ વિભાગ · મિશન કર્મયોગી",
    kn: "ಸಿಬ್ಬಂದಿ ಮತ್ತು ತರಬೇತಿ ಇಲಾಖೆ · ಮಿಷನ್ ಕರ್ಮಯೋಗಿ",
    ml: "പേഴ്സണൽ & ട്രെയിനിംഗ് വകുപ്പ് · മിഷൻ കർമ്മയോഗി",
    pa: "ਪ੍ਰਸੋਨਲ ਅਤੇ ਸਿਖਲਾਈ ਵਿਭਾਗ · ਮਿਸ਼ਨ ਕਰਮਯੋਗੀ"
  },

  // Common UI actions & features
  "Quick Links": {
    hi: "त्वरित लिंक",
    bn: "দ্রুত লিঙ্ক",
    te: "త్వరిత లింకులు",
    ta: "விரைவு இணைப்புகள்",
    mr: "द्रुत लिंक्स",
    gu: "ઝડપી લિંક્સ",
    kn: "ತ್ವರಿತ ಲಿಂಕ್‌ಗಳು",
    ml: "ദ്രുത ലിങ്കുകൾ",
    pa: "ਤੁਰੰਤ ਲਿੰਕ"
  },
  "Contact": {
    hi: "संपर्क",
    bn: "যোগাযোগ",
    te: "సంప్రదించండి",
    ta: "தொடர்புக்கு",
    mr: "संपर्क",
    gu: "સંપર્ક",
    kn: "ಸಂಪರ್ಕ",
    ml: "ബന്ധപ്പെടുക",
    pa: "ਸੰਪਰਕ"
  },
  "Support": {
    hi: "सहायता",
    bn: "সহায়তা",
    te: "మద్దతు",
    ta: "ஆதரவு",
    mr: "सहाय्य",
    gu: "સહાય",
    kn: "ಬೆಂಬಲ",
    ml: "പിന്തുണ",
    pa: "ਸਹਾਇਤਾ"
  },
  "← Back to home": {
    hi: "← होम पर वापस जाएं",
    bn: "← হোমে ফিরে যান",
    te: "← హోమ్‌కి తిరిగి వెళ్ళు",
    ta: "← முகப்புக்குத் திரும்பு",
    mr: "← मुख्यपृष्ठावर परत जा",
    gu: "← હોમ પર પાછા જાઓ",
    kn: "← ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ",
    ml: "← ഹോമിലേക്ക് മടങ്ങുക",
    pa: "← ਮੁੱਖ ਪੰਨੇ 'ਤੇ ਵਾਪਸ ਜਾਓ"
  },
  "← Back to dashboard": {
    hi: "← डैशबोर्ड पर वापस जाएं",
    bn: "← ড্যাশবোর্ডে ফিরে যান",
    te: "← డ్యాష్‌బోర్డ్‌కి తిరిగి వెళ్ళు",
    ta: "← டாஷ்போர்டுக்குத் திரும்பு",
    mr: "← डॅशबोर्डवर परत जा",
    gu: "← ડેશબોર્ડ પર પાછા જાઓ",
    kn: "← ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ",
    ml: "← ഡാഷ്‌ബോർഡിലേക്ക് മടങ്ങുക",
    pa: "← ਡੈਸ਼ਬੋਰਡ 'ਤੇ ਵਾਪਸ ਜਾਓ"
  },
  "← Back to course": {
    hi: "← कोर्स पर वापस जाएं",
    bn: "← কোর্সে ফিরে যান",
    te: "← కోర్సుకు తిరిగి వెళ్ళు",
    ta: "← பாடத்திற்குத் திரும்பு",
    mr: "← अभ्यासक्रमावर परत जा",
    gu: "← કોર્સ પર પાછા જાઓ",
    kn: "← ಕೋರ್ಸ್‌ಗೆ ಹಿಂತಿರುಗಿ",
    ml: "← കോഴ്‌സിലേക്ക് മടങ്ങുക",
    pa: "← ਕੋਰਸ 'ਤੇ ਵਾਪਸ ਜਾਓ"
  },
  "Submit": {
    hi: "जमा करें",
    bn: "জমা দিন",
    te: "సమర్పించు",
    ta: "சமர்ப்பிக்கவும்",
    mr: "सबमिट करा",
    gu: "સબમિટ કરો",
    kn: "ಸಲ್ಲಿಸು",
    ml: "സമർപ്പിക്കുക",
    pa: "ਜਮ੍ਹਾਂ ਕਰੋ"
  },
  "Next": {
    hi: "अगला",
    bn: "পরবর্তী",
    te: "తరువాత",
    ta: "அடுத்து",
    mr: "पुढील",
    gu: "આગળ",
    kn: "ಮುಂದೆ",
    ml: "അടുത്തത്",
    pa: "ਅਗਲਾ"
  },
  "Previous": {
    hi: "पिछला",
    bn: "পূর্ববর্তী",
    te: "మునుపటి",
    ta: "முந்தைய",
    mr: "मागील",
    gu: "પાછળ",
    kn: "ಹಿಂದಿನ",
    ml: "മുമ്പത്തെ",
    pa: "ਪਿਛਲਾ"
  },
  "Cancel": {
    hi: "रद्द करें",
    bn: "বাতিল",
    te: "రద్దు చేయండి",
    ta: "ரத்து செய்",
    mr: "रद्द करा",
    gu: "રદ કરો",
    kn: "ರದ್ದುಮಾಡು",
    ml: "റദ്ദാക്കുക",
    pa: "ਰੱਦ ਕਰੋ"
  },

  // Hands-On Lab & Learning Features
  "Hands-On Lab": {
    hi: "हैंड्स-ऑन लैब (प्रायोगिक अभ्यास)",
    bn: "হ্যান্ডস-অন ল্যাব",
    te: "హ్యాండ్స్-ఆన్ ల్యాబ్",
    ta: "செயல்முறை ஆய்வகம்",
    mr: "हँड्स-ऑन लॅब",
    gu: "હેન્ડ્સ-ઓન લેબ",
    kn: "ಪ್ರಾಯೋಗಿಕ ಲ್ಯಾಬ್",
    ml: "ഹാൻഡ്സ്-ഓൺ ലാബ്",
    pa: "ਹੈਂਡਸ-ਆਨ ਲੈਬ"
  },
  "🧪 Hands-On Lab": {
    hi: "🧪 हैंड्स-ऑन लैब (प्रायोगिक अभ्यास)",
    bn: "🧪 হ্যান্ডস-অন ল্যাব",
    te: "🧪 హ్యాండ్స్-ఆన్ ల్యాబ్",
    ta: "🧪 செயல்முறை ஆய்வகம்",
    mr: "🧪 हँड्स-ऑन लॅब",
    gu: "🧪 હેન્ડ્સ-ઓન લેબ",
    kn: "🧪 ಪ್ರಾಯೋಗಿಕ ಲ್ಯಾಬ್",
    ml: "🧪 ഹാൻഡ്സ്-ഓൺ ലാബ്",
    pa: "🧪 ਹੈਂਡਸ-ਆਨ ਲੈਬ"
  },
  "🚀 Start Hands-On Lab Now →": {
    hi: "🚀 अभी हैंड्स-ऑन लैब शुरू करें →",
    bn: "🚀 এখনই হ্যান্ডস-অন ল্যাব শুরু করুন →",
    te: "🚀 ఇప్పుడే హ్యాండ్స్-ఆన్ ల్యాబ్ ప్రారంభించండి →",
    ta: "🚀 செயல்முறை ஆய்வகத்தை இப்போது தொடங்குங்கள் →",
    mr: "🚀 आताच हँड्स-ऑन लॅब सुरू करा →",
    gu: "🚀 હવે હેન્ડ્સ-ઓન લેબ શરૂ કરો →",
    kn: "🚀 ಈಗಲೇ ಪ್ರಾಯೋಗಿಕ ಲ್ಯಾಬ್ ಪ್ರಾರಂಭಿಸಿ →",
    ml: "🚀 ഇപ്പോൾ ഹാൻഡ്സ്-ഓൺ ലാബ് ആരംഭിക്കുക →",
    pa: "🚀 ਹੁਣੇ ਹੈਂਡਸ-ਆਨ ਲੈਬ ਸ਼ੁਰੂ ਕਰੋ →"
  },
  "Retake Lab": {
    hi: "लैब पुनः दें",
    bn: "ল্যাব পুনরায় দিন",
    te: "ల్యాబ్ మళ్ళీ ప్రయత్నించండి",
    ta: "ஆய்வகத்தை மீண்டும் எடுக்கவும்",
    mr: "लॅब पुन्हा द्या",
    gu: "લેબ ફરીથી આપો",
    kn: "ಲ್ಯಾಬ್ ಮರುಪ್ರಯತ್ನಿಸಿ",
    ml: "ലാബ് വീണ്ടും ചെയ്യുക",
    pa: "ਲੈਬ ਦੁਬਾਰਾ ਕਰੋ"
  },
  "Test Cases": {
    hi: "परीक्षण स्थितियां (Test Cases)",
    bn: "টেস্ট কেস",
    te: "టెస్ట్ కేసులు",
    ta: "சோதனை நிகழ்வுகள்",
    mr: "टेस्ट केसेस",
    gu: "ટેસ્ટ કેસ",
    kn: "ಟೆಸ್ಟ್ ಕೇಸ್‌ಗಳು",
    ml: "ടെസ്റ്റ് കേസുകൾ",
    pa: "ਟੈਸਟ ਕੇਸ"
  },
  "▶ Run & Test": {
    hi: "▶ चलाएं और जांचें",
    bn: "▶ রান ও টেস্ট করুন",
    te: "▶ రన్ & టెస్ట్ చేయండి",
    ta: "▶ இயக்கி சோதிக்கவும்",
    mr: "▶ चालवा आणि चाचणी करा",
    gu: "▶ ચલાવો અને ચકાસો",
    kn: "▶ ರನ್ ಮಾಡಿ ಮತ್ತು ಪರೀಕ್ಷಿಸಿ",
    ml: "▶ റൺ ചെയ്ത് പരിശോധിക്കുക",
    pa: "▶ ਚਲਾਓ ਅਤੇ ਟੈਸਟ ਕਰੋ"
  },
  "Reset": {
    hi: "रीसेट",
    bn: "রিসেট",
    te: "రీసెట్",
    ta: "மீட்டமை",
    mr: "रीसेट",
    gu: "રીસેટ",
    kn: "ಮರುಹೊಂದಿಸಿ",
    ml: "റീസെറ്റ്",
    pa: "ਰੀਸੈੱਟ"
  },
  "Clear": {
    hi: "साफ़ करें",
    bn: "মুছুন",
    te: "క్లియర్ చేయండి",
    ta: "அழிக்கவும்",
    mr: "साफ करा",
    gu: "સાફ કરો",
    kn: "ತೆರವುಗೊಳಿಸಿ",
    ml: "മായ്ക്കുക",
    pa: "ਸਾਫ਼ ਕਰੋ"
  },
  "Submit Lab": {
    hi: "लैब सबमिट करें",
    bn: "ল্যাব জমা দিন",
    te: "ల్యాబ్ సమర్పించండి",
    ta: "ஆய்வகத்தை சமர்ப்பிக்கவும்",
    mr: "लॅब सबमिट करा",
    gu: "લેબ સબમિટ કરો",
    kn: "ಲ್ಯಾಬ್ ಸಲ್ಲಿಸಿ",
    ml: "ലാബ് സമർപ്പിക്കുക",
    pa: "ਲੈਬ ਜਮ੍ਹਾਂ ਕਰੋ"
  },
  "Next Problem →": {
    hi: "अगला प्रश्न →",
    bn: "পরবর্তী সমস্যা →",
    te: "తరువాతి సమస్య →",
    ta: "அடுத்த கணக்கு →",
    mr: "पुढील समस्या →",
    gu: "આગળનો પ્રશ્ન →",
    kn: "ಮುಂದಿನ ಸಮಸ್ಯೆ →",
    ml: "അടുത്ത പ്രശ്നം →",
    pa: "ਅਗਲੀ ਸਮੱਸਿਆ →"
  },
  "← Previous": {
    hi: "← पिछला",
    bn: "← পূর্ববর্তী",
    te: "← మునుపటి",
    ta: "← முந்தைய",
    mr: "← मागील",
    gu: "← પાછળ",
    kn: "← ಹಿಂದಿನ",
    ml: "← മുമ്പത്തെ",
    pa: "← ਪਿਛਲਾ"
  },
  "Show hints": {
    hi: "संकेत देखें",
    bn: "ইঙ্গিত দেখুন",
    te: "సూచనలు చూపించు",
    ta: "குறிப்புகளைக் காட்டு",
    mr: "इशारे पहा",
    gu: "સંકેતો જુઓ",
    kn: "ಸುಳಿವುಗಳನ್ನು ತೋರಿಸಿ",
    ml: "സൂചനകൾ കാണിക്കുക",
    pa: "ਸੰਕੇਤ ਵੇਖੋ"
  },
  "Course progress": {
    hi: "कोर्स की प्रगति",
    bn: "কোর্সের অগ্রগতি",
    te: "కోర్సు పురోగతి",
    ta: "பாடநெறி முன்னேற்றம்",
    mr: "अभ्यासक्रमाची प्रगती",
    gu: "કોર્સની પ્રગતિ",
    kn: "ಕೋರ್ಸ್ ಪ್ರಗತಿ",
    ml: "കോഴ്‌സ് പുരോഗതി",
    pa: "ਕੋਰਸ ਦੀ ਪ੍ਰਗਤੀ"
  },
  "Quiz": {
    hi: "प्रश्नोत्तरी (क्विज़)",
    bn: "কুইজ",
    te: "క్విజ్",
    ta: "வினாடி வினா",
    mr: "क्विझ",
    gu: "ક્વિઝ",
    kn: "ರಸಪ್ರಶ್ನೆ",
    ml: "ക്വിസ്",
    pa: "ਕਵਿਜ਼"
  },
  "Competency Assessment": {
    hi: "योग्यता मूल्यांकन",
    bn: "দক্ষতা মূল্যায়ন",
    te: "సామర్థ్య అంచనా",
    ta: "திறன் மதிப்பீடு",
    mr: "क्षमता मूल्यमापन",
    gu: "ક્ષમતા મૂલ્યાંકન",
    kn: "ಸಾಮರ್ಥ್ಯ ಮೌಲ್ಯಮಾಪನ",
    ml: "യോഗ്യതാ വിലയിരുത്തൽ",
    pa: "ਯੋਗਤਾ ਮੁਲਾਂਕਣ"
  },
  "learning hrs": {
    hi: "अध्ययन के घंटे",
    bn: "শেখার সময় (ঘণ্টা)",
    te: "అభ్యాస గంటలు",
    ta: "கற்றல் மணிநேரம்",
    mr: "अध्ययन तास",
    gu: "શીખવાના કલાકો",
    kn: "ಕಲಿಕೆಯ ಗಂಟೆಗಳು",
    ml: "പഠന സമയം (മണിക്കൂർ)",
    pa: "ਸਿੱਖਣ ਦੇ ਘੰਟੇ"
  },
  "courses": {
    hi: "पाठ्यक्रम (कोर्स)",
    bn: "কোর্সসমূহ",
    te: "కోర్సులు",
    ta: "பாடநெறிகள்",
    mr: "अभ्यासक्रम",
    gu: "કોર્સ",
    kn: "ಕೋರ್ಸ್‌ಗಳು",
    ml: "കോഴ്‌സുകൾ",
    pa: "ਕੋਰਸ"
  },
  "open gaps": {
    hi: "सुधार योग्य कमियां",
    bn: "দক্ষতার ব্যবধান",
    te: "సామర్థ్య లోపాలు",
    ta: "திறன் இடைவெளிகள்",
    mr: "क्षमतेतील अंतर",
    gu: "ક્ષમતા અંતર",
    kn: "ತೆರೆದ ಅಂತರಗಳು",
    ml: "തുറന്ന വിടവുകൾ",
    pa: "ਸੁਧਾਰ ਯੋਗ ਪਾੜੇ"
  },
  "readiness": {
    hi: "तैयारी प्रतिशत",
    bn: "প্রস্তুতি",
    te: "సన్నద్ధత",
    ta: "தயார்நிலை",
    mr: "सज्जता",
    gu: "તૈયારી",
    kn: "ಸಿದ್ಧತೆ",
    ml: "സന്നദ്ധത",
    pa: "ਤਿਆਰੀ"
  }
};

/**
 * Get the currently active language code from localStorage, default to 'en'
 */
function getCurrentLanguage() {
  return localStorage.getItem("igot_lang") || "en";
}

/**
 * Switch language, save to localStorage and translate the page
 */
function setLanguage(langCode) {
  localStorage.setItem("igot_lang", langCode);
  applyTranslations(langCode);
  updateLanguageDropdowns(langCode);
}

/**
 * Translate a single string or return the original text
 */
function t(text, lang) {
  lang = lang || getCurrentLanguage();
  if (lang === "en") return text;
  const entry = I18N_DICTIONARY[text.trim()];
  if (entry && entry[lang]) {
    return entry[lang];
  }
  return text;
}

/**
 * Cache for dynamic translations per language in sessionStorage
 */
function getTranslationCache(lang) {
  try {
    const raw = sessionStorage.getItem("igot_trans_cache_" + lang);
    return raw ? JSON.parse(raw) : {};
  } catch(e) {
    return {};
  }
}

function saveTranslationCache(lang, cache) {
  try {
    sessionStorage.setItem("igot_trans_cache_" + lang, JSON.stringify(cache));
  } catch(e) {}
}

/**
 * Dynamically translate an array of texts using /api/translate endpoint with local caching
 */
async function translateDynamicTexts(texts, lang) {
  lang = lang || getCurrentLanguage();
  if (lang === "en" || !texts || !texts.length) return texts;

  const cache = getTranslationCache(lang);
  const toFetch = [];
  const toFetchIndices = [];

  const results = texts.map((t, idx) => {
    const trimmed = (t || "").trim();
    if (!trimmed || trimmed.length <= 1) return t;

    // Check static dictionary first
    if (I18N_DICTIONARY[trimmed] && I18N_DICTIONARY[trimmed][lang]) {
      return I18N_DICTIONARY[trimmed][lang];
    }
    // Check local session cache
    if (cache[trimmed]) {
      return cache[trimmed];
    }
    // Need translation
    toFetch.push(trimmed);
    toFetchIndices.push(idx);
    return t;
  });

  if (toFetch.length > 0) {
    let handled = false;
    // 1. Try backend /api/translate first
    try {
      const apiBase = window.IGOT_API_BASE || (["localhost", "127.0.0.1"].includes(location.hostname) ? "http://localhost:8001" : "https://igot-karmayogi-zs8h.onrender.com");
      const resp = await fetch(apiBase + "/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texts: toFetch, target_lang: lang })
      });
      if (resp.ok) {
        const data = await resp.json();
        const translatedList = data.translated || [];
        translatedList.forEach((trans, i) => {
          const original = toFetch[i];
          if (trans && trans !== original) {
            cache[original] = trans;
            results[toFetchIndices[i]] = trans;
          }
        });
        saveTranslationCache(lang, cache);
        handled = true;
      }
    } catch(err) {
      // Backend not running or offline, proceed to client-side direct translation
    }

    // 2. Client-side fallback via Google GTX API directly (runs in browser, fast, no CORS issues)
    if (!handled) {
      await Promise.all(toFetch.map(async (text, i) => {
        try {
          const q = encodeURIComponent(text.slice(0, 500));
          const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${lang}&dt=t&q=${q}`;
          const res = await fetch(url);
          if (res.ok) {
            const data = await res.json();
            if (data && data[0]) {
              const trans = data[0].map(s => s[0]).join("");
              if (trans) {
                cache[text] = trans;
                results[toFetchIndices[i]] = trans;
              }
            }
          }
        } catch(e) {
          // Fallback to MyMemory if GTX fails
          try {
            const q = encodeURIComponent(text.slice(0, 500));
            const url = `https://api.mymemory.translated.net/get?q=${q}&langpair=en|${lang}`;
            const res = await fetch(url);
            if (res.ok) {
              const data = await res.json();
              const trans = data.responseData && data.responseData.translatedText;
              if (trans && !trans.startsWith("MYMEMORY WARNING")) {
                cache[text] = trans;
                results[toFetchIndices[i]] = trans;
              }
            }
          } catch(e2) {}
        }
      }));
      saveTranslationCache(lang, cache);
    }
  }

  return results;
}
window.translateDynamicTexts = translateDynamicTexts;

/**
 * Translate a container element's contents dynamically (including text nodes and placeholders)
 */
async function translateDynamicElement(container, lang) {
  if (!container) return;
  lang = lang || getCurrentLanguage();
  if (lang === "en") {
    // Restore original text if preserved
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
    while (walker.nextNode()) {
      if (walker.currentNode.__origText) {
        walker.currentNode.nodeValue = walker.currentNode.__origText;
      }
    }
    container.querySelectorAll('[data-orig-text]').forEach(el => {
      el.textContent = el.getAttribute('data-orig-text');
    });
    return;
  }

  // 1. Gather all text nodes that are not inside code editors or scripts
  const walker = document.createTreeWalker(
    container,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tag = parent.tagName.toLowerCase();
        if (tag === 'script' || tag === 'style' || tag === 'noscript' || tag === 'textarea' || tag === 'pre' || tag === 'code') {
          return NodeFilter.FILTER_REJECT;
        }
        if (parent.closest('#monaco-editor-container') || parent.closest('#editor-container') || parent.closest('.monaco-editor')) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  const textNodes = [];
  while (walker.nextNode()) {
    textNodes.push(walker.currentNode);
  }

  const textsToTranslate = [];
  const nodesToTranslate = [];

  textNodes.forEach(node => {
    if (!node.__origText) {
      node.__origText = node.nodeValue;
    }
    const orig = node.__origText.trim();
    if (I18N_DICTIONARY[orig] && I18N_DICTIONARY[orig][lang]) {
      node.nodeValue = node.__origText.replace(orig, I18N_DICTIONARY[orig][lang]);
    } else if (orig.length > 1) {
      textsToTranslate.push(orig);
      nodesToTranslate.push(node);
    }
  });

  if (textsToTranslate.length > 0) {
    const translated = await translateDynamicTexts(textsToTranslate, lang);
    translated.forEach((trans, i) => {
      const node = nodesToTranslate[i];
      if (node && trans) {
        node.nodeValue = node.__origText.replace(textsToTranslate[i], trans);
      }
    });
  }

  // Also translate input placeholders
  container.querySelectorAll('input[placeholder]').forEach(async input => {
    const ph = input.getAttribute('placeholder');
    if (!input.getAttribute('data-orig-ph')) {
      input.setAttribute('data-orig-ph', ph);
    }
    const orig = input.getAttribute('data-orig-ph');
    const [trans] = await translateDynamicTexts([orig], lang);
    if (trans) input.setAttribute('placeholder', trans);
  });
}
window.translateDynamicElement = translateDynamicElement;

/**
 * Scan DOM text nodes and placeholder attributes and apply dictionary translations
 */
async function applyTranslations(lang) {
  lang = lang || getCurrentLanguage();
  document.documentElement.lang = lang;

  // Walk text nodes in body
  await translateDynamicElement(document.body, lang);
}
window.applyTranslations = applyTranslations;

/**
 * Render the language selector dropdown component
 */
function renderLanguageDropdown(compact = false) {
  const current = getCurrentLanguage();
  const activeLang = SUPPORTED_LANGUAGES.find(l => l.code === current) || SUPPORTED_LANGUAGES[0];

  return `
  <div class="relative inline-block text-left language-picker-root" style="z-index: 55;">
    <button type="button" onclick="toggleLanguageMenu(this, event)"
            class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-full border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 shadow-sm transition-all focus:outline-none"
            aria-label="Change language">
      <span class="text-sm leading-none">🌐</span>
      <span class="lang-label font-medium">${activeLang.name}</span>
      <svg class="w-3.5 h-3.5 text-slate-400 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>
    <div class="lang-dropdown-menu hidden absolute right-0 mt-2 w-44 rounded-xl bg-white shadow-xl border border-slate-100 py-1.5 ring-1 ring-black ring-opacity-5 focus:outline-none max-h-72 overflow-y-auto"
         style="z-index: 100;">
      <div class="px-3 py-1 border-b border-slate-100 text-[10px] font-bold tracking-wider text-slate-400 uppercase">
        Select Language (10)
      </div>
      ${SUPPORTED_LANGUAGES.map(l => `
        <button type="button" onclick="selectLanguage('${l.code}', event)"
                class="w-full text-left px-3.5 py-2 text-xs flex items-center justify-between hover:bg-blue-50 transition-colors ${l.code === current ? 'bg-blue-50/70 text-blue-700 font-bold' : 'text-slate-700'}">
          <span>${l.name}</span>
          <span class="text-[10px] text-slate-400">${l.label}</span>
        </button>
      `).join('')}
    </div>
  </div>`;
}

function toggleLanguageMenu(btn, ev) {
  if (ev) ev.stopPropagation();
  const root = btn.closest('.language-picker-root');
  if (!root) return;
  const menu = root.querySelector('.lang-dropdown-menu');
  if (!menu) return;

  // close other open menus
  document.querySelectorAll('.lang-dropdown-menu').forEach(m => {
    if (m !== menu) m.classList.add('hidden');
  });

  menu.classList.toggle('hidden');
}

function selectLanguage(code, ev) {
  if (ev) ev.stopPropagation();
  setLanguage(code);
  document.querySelectorAll('.lang-dropdown-menu').forEach(m => m.classList.add('hidden'));
}

function updateLanguageDropdowns(langCode) {
  const activeLang = SUPPORTED_LANGUAGES.find(l => l.code === langCode) || SUPPORTED_LANGUAGES[0];
  document.querySelectorAll('.language-picker-root').forEach(root => {
    const label = root.querySelector('.lang-label');
    if (label) label.textContent = activeLang.name;
    root.querySelectorAll('.lang-dropdown-menu button').forEach(btn => {
      btn.classList.remove('bg-blue-50/70', 'text-blue-700', 'font-bold');
    });
  });
}

// Global click listener to close dropdown when clicking outside
if (typeof window !== "undefined") {
  window.addEventListener("click", function(e) {
    if (!e.target.closest('.language-picker-root')) {
      document.querySelectorAll('.lang-dropdown-menu').forEach(m => m.classList.add('hidden'));
    }
  });

  // Automatically apply stored language once DOM is ready
  document.addEventListener("DOMContentLoaded", function() {
    const lang = getCurrentLanguage();
    if (lang !== "en") {
      setTimeout(() => applyTranslations(lang), 100);
    }
  });

  // Observe dynamically added modals and popup elements
  let debounceTimeout = null;
  const observer = new MutationObserver(mutations => {
    const lang = getCurrentLanguage();
    if (lang === "en") return;

    let hasSignificantNewNodes = false;
    for (const mutation of mutations) {
      if (mutation.addedNodes.length > 0) {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Ignore Monaco editor internals or script/style
            if (node.closest && (node.closest('#monaco-editor-container') || node.closest('#editor-container') || node.closest('.monaco-editor'))) {
              continue;
            }
            if (['SCRIPT', 'STYLE', 'TEXTAREA'].includes(node.tagName)) continue;
            hasSignificantNewNodes = true;
            break;
          }
        }
      }
      if (hasSignificantNewNodes) break;
    }

    if (hasSignificantNewNodes) {
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(() => {
        applyTranslations(lang);
      }, 350);
    }
  });

  document.addEventListener("DOMContentLoaded", function() {
    observer.observe(document.body, { childList: true, subtree: true });
  });
}
