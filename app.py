import streamlit as st
import requests
from deep_translator import GoogleTranslator
import pandas as pd
import plotly.express as px

# --- 1. الإعدادات والتنسيق الجمالي (CSS) ---
st.set_page_config(page_title="منصة أسامة المتكاملة", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* تلوين القائمة الجانبية والنصوص بداخلها */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important;
    }
    [data-testid="stSidebar"] *, [data-testid="stSidebarNavSeparator"] {
        color: white !important;
    }
    
    /* تلوين السهم العلوي والأيقونات */
    button[kind="header"], .st-emotion-cache-15ec669 {
        color: white !important;
    }

    /* تصميم البطاقة الزجاجية لنتائج الترجمة */
    .result-card {
        background: rgba(0, 122, 255, 0.15);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid rgba(0, 122, 255, 0.4);
        backdrop-filter: blur(10px);
        margin-top: 20px;
        text-align: right;
    }

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070");
        background-size: cover;
    }
    h1, h2, h3, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.markdown("## 🛡️ نظام أسامة الذكي")
    choice = st.selectbox("القائمة المنسدلة:", [
        "✍️ المترجم النصي العالمي",
        "💰 محول العملات والتحليل",
        "📸 الترجمة المرئية (OCR)",
        "🔍 فاحص الأمان"
    ])
    st.write("---")
    st.info("👤 المطور: **اسامه قراوط**")

# --- 3. تشغيل الميزات ---

if choice == "✍️ المترجم النصي العالمي":
    st.title("✍️ المترجم الذكي الشامل")
    text_input = st.text_area("أدخل النص هنا:", height=150)
    
    # قائمة اللغات
    langs = {'العربية': 'ar', 'الإنجليزية': 'en', 'الفرنسية': 'fr', 'التركية': 'tr', 'الألمانية': 'de'}
    target = st.selectbox("اختر لغة الهدف:", list(langs.keys()))
    
    if st.button("ترجمة النص ✨"):
        if text_input:
            with st.spinner("جاري المعالجة..."):
                translation = GoogleTranslator(source='auto', target=langs[target]).translate(text_input)
                # عرض النتيجة داخل البطاقة الزجاجية
                st.markdown(f"""
                    <div class="result-card">
                        <h3 style="color: #007AFF !important;">✅ النتيجة:</h3>
                        <p style="font-size: 1.2em; line-height: 1.6;">{translation}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة نص للبدء.")

# --- 4. التذييل (Footer) ---
st.markdown("<br><br><p style='text-align: center; color: #888;'>🚀 جميع الحقوق محفوظة لـ <b>أسامة قراوط</b> &copy; 2026</p>", unsafe_allow_html=True)
countries = {
    "967": {"name": "اليمن", "flag": "🇾🇪"},
    "966": {"name": "السعودية", "flag": "🇸🇦"},
    "20":  {"name": "مصر", "flag": "🇪🇬"},
    "971": {"name": "الإمارات", "flag": "🇦🇪"}
}
if code in countries:
    # هنا نكتب ما سيحدث إذا وجدنا الدولة
    name = countries[code]["name"]
    flag = countries[code]["flag"]
    st.success(f"الدولة المكتشفة: {name} {flag}")
else:
    # هنا نكتب ما سيحدث إذا لم نجد الرمز في قائمتنا
    st.warning("عذراً، رمز الدولة هذا غير مسجل لدينا حالياً.")
# قائمة بالكلمات المشبوهة التي قد تدل على تصيد احتيالي
suspicious_words = ["login", "verify", "bit.ly", "update", "bank", "free"]

url_input = st.text_input("أدخل الرابط للفحص:")

if st.button("بدء الفحص العميق 🔍"):
    if url_input:
        is_suspicious = False
        found_word = ""
        
        # حلقة فحص للبحث عن الكلمات المشبوهة
        for word in suspicious_words:
            if word in url_input.lower(): # هنا استخدمنا "in" بدلاً من الفراغ
                is_suspicious = True
                found_word = word
                break
        
        # عرض النتيجة في بطاقة زجاجية
        if is_suspicious:
            st.error(f"⚠️ تحذير: هذا الرابط مشبوه جداً! يحتوي على كلمة: {found_word}")
        else:
            st.success("✅ الرابط يبدو آمناً بناءً على الفحص الأولي.")
    else:
        st.warning("الرجاء إدخال رابط أولاً.")
phone_data = {
    "967": {
        "country": "اليمن",
        "flag": "🇾🇪",
        "operators": ["SabaFon", "MTN", "Yemen Mobile"],
        "type": "Mobile/Landline"
    },
    "966": {
        "country": "السعودية",
        "flag": "🇸🇦",
        "operators": ["STC", "Mobily", "Zain"],
        "type": "Mobile"
    }
}
if not url.startswith("https://"):
    st.warning("⚠️ تحذير: هذا الرابط غير مشفر (لا يستخدم HTTPS)")
st.sidebar.title("دعم المشروع ☕")
st.sidebar.write("إذا أعجبك التطبيق، يمكنك دعمنا لنستمر في تطوير ميزات احترافية جديدة.")
st.sidebar.link_button("🚀 ادعم المطور الآن", "https://www.buymeacoffee.com/yourusername")
# فحص إذا كان الرابط يحتوي على كلمة مشبوهة *أو* لا يبدأ ببروتوكول آمن
if (any(word in url_input.lower() for word in suspicious_words)) or (not url_input.startswith("https://")):
    st.error("⚠️ تحذير أمني: الرابط قد يكون خطيراً!")
uploaded_file = st.file_uploader("اختر ملفاً لفحصه 📂", type=["jpg", "png", "pdf", "docx", "zip"])

if uploaded_file is not None:
    # هنا سنقوم بكتابة عمليات الفحص
    file_details = {"اسم الملف": uploaded_file.name, "الحجم": uploaded_file.size}
    st.write(file_details)
# قائمة بالملفات الخطيرة التي سنحذر منها حتى لو رُفعت
dangerous_extensions = [".exe", ".php", ".js", ".scr"]

if uploaded_file is not None:
    file_name = uploaded_file.name.lower()
    
    # التحقق إذا كان الملف ينتهي بامتداد خطر
    is_dangerous = False
    for ext in dangerous_extensions:
        if file_name.endswith(ext):
            is_dangerous = True
            break
            
    if is_dangerous:
        st.error("❌ تحذير: هذا النوع من الملفات قد يلحق الضرر بجهازك!")
    else:
        st.success("✅ امتداد الملف يبدو آمناً.")
if uploaded_file.size > max_size:
    st.warning("⚠️ تنبيه: حجم الملف كبير جداً، قد يستغرق فحص الفيروسات وقتاً أطول.")
if uploaded_file.size > max_size:
    st.warning("⚠️ تنبيه: حجم الملف كبير جداً، قد يستغرق فحص الفيروسات وقتاً أطول.")
