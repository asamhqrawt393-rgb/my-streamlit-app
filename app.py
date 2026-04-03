import streamlit as st
import requests
from deep_translator import GoogleTranslator

# --- 1. الإعدادات والتنسيق الجمالي (CSS) ---
st.set_page_config(page_title="منصة أسامة المتكاملة", page_icon="🛡️", layout="wide")

# تعريف المتغيرات الأساسية لتجنب الأخطاء
max_size = 10 * 1024 * 1024  # 10 ميجابايت
countries = {
    "967": {"name": "اليمن", "flag": "🇾🇪"},
    "966": {"name": "السعودية", "flag": "🇸🇦"},
    "20":  {"name": "مصر", "flag": "🇪🇬"},
    "971": {"name": "الإمارات", "flag": "🇦🇪"}
}
suspicious_words = ["login", "verify", "bit.ly", "update", "bank", "free"]

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #001f3f !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070");
        background-size: cover;
    }
    .glass-card {
        background: rgba(0, 50, 100, 0.2); 
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(0, 122, 255, 0.3);
        margin-bottom: 20px;
    }
    h1, h2, h3, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.markdown("## 🛡️ نظام أسامة الذكي")
    choice = st.selectbox("اختر الأداة:", [
        "✍️ المترجم النصي العالمي",
        "🔍 فاحص الأمان والملفات",
        "📱 كاشف الأرقام الذكي"
    ])
    st.write("---")
    st.sidebar.link_button("🚀 ادعم المطور الآن", "https://www.buymeacoffee.com/yourusername")
    st.info("👤 المطور: **اسامه قراوط**")

# --- 3. تشغيل الميزات ---

if choice == "✍️ المترجم النصي العالمي":
    st.title("✍️ المترجم الذكي الشامل")
    text_input = st.text_area("أدخل النص هنا:")
    target = st.selectbox("اختر لغة الهدف:", ['ar', 'en', 'fr', 'tr', 'de'])
    if st.button("ترجمة الآن ✨"):
        if text_input:
            translation = GoogleTranslator(source='auto', target=target).translate(text_input)
            st.success(f"النتيجة: {translation}")

elif choice == "🔍 فاحص الأمان والملفات":
    st.title("🔍 فاحص الروابط والملفات")
    
    # فحص الروابط
    url_input = st.text_input("أدخل الرابط للفحص:")
    if st.button("بدء فحص الرابط 🔍"):
        is_unsafe = any(word in url_input.lower() for word in suspicious_words)
        if is_unsafe or not url_input.startswith("https://"):
            st.error("⚠️ تحذير: الرابط قد يكون خطيراً أو غير مشفر!")
        else:
            st.success("✅ الرابط يبدو آمناً.")

    st.write("---")
    
    # فحص الملفات (إصلاح الخطأ هنا)
    uploaded_file = st.file_uploader("اختر ملفاً لفحصه 📂")
    if uploaded_file is not None:
        # لا نصل لـ .size إلا إذا كان الملف موجوداً فعلاً
        if uploaded_file.size > max_size:
            st.warning("⚠️ تنبيه: حجم الملف كبير جداً!")
        else:
            st.success(f"✅ الملف {uploaded_file.name} جاهز وآمن.")

elif choice == "📱 كاشف الأرقام الذكي":
    st.title("📱 كاشف الأرقام")
    code_input = st.text_input("أدخل مفتاح الدولة (مثلاً 967):")
    if st.button("كشف 🔍"):
        if code_input in countries:
            res = countries[code_input]
            st.success(f"الدولة: {res['name']} {res['flag']}")
        else:
            st.warning("عذراً، هذا المفتاح غير مسجل.")

# --- 4. التذييل ---
st.markdown("<p style='text-align: center; color: #888;'>🚀 جميع الحقوق محفوظة لأسامة قراوط &copy; 2026</p>", unsafe_allow_html=True)
