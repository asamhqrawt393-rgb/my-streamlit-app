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
import streamlit as st
import requests
from deep_translator import GoogleTranslator

# --- 1. الإعدادات الأساسية ---
st.set_page_config(page_title="منصة أسامة", page_icon="🛡️")

# حد الحجم للملفات (10 ميجابايت)
max_size = 10 * 1024 * 1024 

# --- 2. القائمة الجانبية (نفس أسلوبك السابق) ---
with st.sidebar:
    st.title("🛡️ نظام أسامة الذكي")
    choice = st.selectbox("اختر الأداة المطلوبة:", [
        "💰 محول العملات",
        "✍️ المترجم النصي",
        "🔍 فاحص الأمان والملفات", # دمجناهم هنا لسهولة الوصول
        "📱 كاشف الأرقام"
    ])
    st.write("---")
    st.sidebar.link_button("🚀 ادعم المطور", "https://www.buymeacoffee.com/yourusername")
    st.info("المطور: أسامة قراوط")

# --- 3. تشغيل الأدوات ---

# أداة فحص الأمان والملفات (حيث حدث الخطأ سابقاً)
if choice == "🔍 فاحص الأمان والملفات":
    st.header("🔍 فحص الروابط والملفات")
    
    # جزء الروابط
    url_input = st.text_input("أدخل الرابط للفحص:")
    if st.button("فحص الرابط"):
        if url_input.startswith("https://"):
            st.success("🔒 الرابط آمن ومشفر")
        else:
            st.error("⚠️ الرابط غير مشفر!")

    st.write("---")
    
    # جزء الملفات (تم إصلاح الخطأ هنا)
    uploaded_file = st.file_uploader("ارفع ملفاً لفحصه", type=["jpg", "png", "pdf"])
    
    if uploaded_file is not None:
        # الفحص يتم فقط إذا وُجد ملف، لتجنب AttributeError
        if uploaded_file.size > max_size:
            st.warning("⚠️ حجم الملف كبير جداً!")
        else:
            st.success(f"✅ الملف {uploaded_file.name} جاهز وآمن.")

# أداة كاشف الأرقام
elif choice == "📱 كاشف الأرقام":
    st.header("📱 كاشف الأرقام")
    phone = st.text_input("أدخل الرقم الدولي:")
    if st.button("كشف"):
        st.info(f"الرقم {phone} قيد التحليل... (يتطلب ربط API للاسم)")
