import streamlit as st
import requests
from deep_translator import GoogleTranslator
import easyocr
from PIL import Image
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import time
import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(page_title="منصة أسامة الأمنية", page_icon="🛡️", layout="wide")

# حجم الملف الأقصى (10 ميجابايت)
max_size = 10 * 1024 * 1024 

# قاعدة بيانات الدول (القاموس المتداخل)
phone_data = {
    "967": {"country": "اليمن", "flag": "🇾🇪", "lat": 15.5527, "lon": 48.5164},
    "966": {"country": "السعودية", "flag": "🇸🇦", "lat": 23.8859, "lon": 45.0792},
    "20":  {"name": "مصر", "flag": "🇪🇬", "lat": 26.8206, "lon": 30.8025},
}

# تنسيق CSS احترافي
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #001f3f !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stApp { background-color: #050a10; }
    .glass-card {
        background: rgba(0, 122, 255, 0.1);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(0, 122, 255, 0.3);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة سجل العمليات (Session State) ---
if 'history' not in st.session_state:
    st.session_state.history = []

def add_to_history(item):
    st.session_state.history.insert(0, item)
    if len(st.session_state.history) > 5:
        st.session_state.history.pop()

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.title("🛡️ نظام أسامة الذكي")
    st.sidebar.link_button("🚀 ادعم المطور الآن", "https://www.buymeacoffee.com/yourusername")
    st.write("---")
    st.subheader("آخر العمليات 🕒")
    for item in st.session_state.history:
        st.write(f"• {item}")
    st.write("---")
    st.info("المطور: أسامة قراوط")

# --- 4. الواجهة الرئيسية (الألسنة) ---
tab1, tab2, tab3 = st.tabs(["📱 كاشف الأرقام", "🔗 فحص الروابط", "📂 فحص الملفات"])

# التبويب الأول: كاشف الأرقام
with tab1:
    st.markdown("<div class='glass-card'><h2>📱 كاشف وتحليل الأرقام</h2></div>", unsafe_allow_html=True)
    phone_input = st.text_input("أدخل الرقم (مثلاً 967...):")
    
    if st.button("تحليل الرقم 🔍"):
        if phone_input:
            # محاولة استخراج رمز الدولة من أول 3 أو 2 أرقام
            found_code = None
            for code in phone_data.keys():
                if phone_input.startswith(code):
                    found_code = code
                    break
            
            if found_code:
                data = phone_data[found_code]
                st.success(f"✅ تم التعرف على الدولة: {data['country']} {data['flag']}")
                # عرض الخريطة
                map_df = pd.DataFrame({'lat': [data['lat']], 'lon': [data['lon']]})
                st.map(map_df)
                add_to_history(f"رقم من {data['country']}")
            else:
                st.error("❌ رمز الدولة غير مسجل في النظام حالياً.")
        else:
            st.warning("الرجاء إدخال رقم أولاً.")

# التبويب الثاني: فحص الروابط
with tab2:
    st.markdown("<div class='glass-card'><h2>🔗 رادار الروابط المشبوهة</h2></div>", unsafe_allow_html=True)
    url_input = st.text_input("أدخل الرابط للفحص:")
    suspicious_words = ["login", "verify", "bit.ly", "bank", "free"]

    if st.button("فحص الرابط 🛡️"):
        if url_input:
            is_unsafe = any(word in url_input.lower() for word in suspicious_words)
            is_not_https = not url_input.startswith("https://")
            
            if is_unsafe or is_not_https:
                st.error("⚠️ تحذير: الرابط قد يكون خطيراً أو غير مشفر!")
            else:
                st.success("✅ الرابط يبدو آمناً.")
            add_to_history(f"فحص رابط: {url_input[:20]}...")
        else:
            st.warning("الرجاء إدخال رابط.")

# التبويب الثالث: فحص الملفات
with tab3:
    st.markdown("<div class='glass-card'><h2>📂 فاحص الملفات المتقدم</h2></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملفاً لفحصه", type=["jpg", "png", "pdf", "zip"])
    
    if uploaded_file is not None:
        # صمام الأمان: فحص الحجم داخل شرط الوجود
        if uploaded_file.size > max_size:
            st.error(f"❌ الملف كبير جداً! الحجم الحالي: {uploaded_file.size / (1024*1024):.1f} MB")
        else:
            st.success(f"✅ تم رفع {uploaded_file.name} بنجاح. الحجم آمن.")
            add_to_history(f"ملف: {uploaded_file.name}")

# التذييل
st.markdown("<p style='text-align: center; color: grey;'>جميع الحقوق محفوظة لأسامة قراوط © 2026</p>", unsafe_allow_html=True)
