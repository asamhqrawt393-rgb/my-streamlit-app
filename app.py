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
