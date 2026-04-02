import streamlit as st
import requests
from deep_translator import GoogleTranslator
import easyocr
from PIL import Image
import numpy as np

# --- تحسين المظهر والألوان ---
st.set_page_config(page_title="التطبيق الشامل الذكي", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029");
        background-size: cover;
    }
    /* جعل كل النصوص بيضاء وواضحة جداً */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }
    /* تحسين لون الأزرار لتبدو واضحة */
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
    }
    /* جعل الكتابة داخل الصناديق سوداء لسهولة القراءة */
    input, textarea {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- القائمة الجانبية ---
st.sidebar.title("🛠️ الأدوات الذكية")
choice = st.sidebar.selectbox("اختر الأداة:", 
    ["🌐 المترجم النصي", "📸 مترجم الصور (OCR)", "📝 ملخص النصوص", "💰 محول العملات", "🔍 فاحص الروابط"])

# --- ميزة محول العملات (نسخة محسنة) ---
if choice == "💰 محول العملات":
    st.header("💰 محول العملات المباشر")
    amount = st.number_input("المبلغ:", min_value=1.0, value=100.0)
    from_c = st.text_input("من عملة (مثل USD):", "USD").upper()
    to_c = st.text_input("إلى عملة (مثل SAR):", "SAR").upper()
    
    if st.button("تحويل الآن"):
        try:
            # استخدام خدمة بديلة وأكثر استقراراً
            url = f"https://open.er-api.com/v6/latest/{from_c}"
            data = requests.get(url).json()
            if data['result'] == 'success':
                rate = data['rates'][to_c]
                res = amount * rate
                st.success(f"✅ {amount} {from_c} = {res:.2f} {to_c}")
            else:
                st.error("❌ تأكد من رموز العملات.")
        except:
            st.error("⚠️ فشل الاتصال بالخدمة، حاول مجدداً.")

# (بقية الميزات تظل كما هي في الكود السابق)
