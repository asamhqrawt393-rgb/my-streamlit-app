import streamlit as st
import requests
from deep_translator import GoogleTranslator
import easyocr
from PIL import Image
import numpy as np

# --- 1. إعداد مظهر التطبيق (الخلفية) ---
st.set_page_config(page_title="التطبيق الشامل", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029");
        background-size: cover;
    }
    .main { color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. القائمة الجانبية ---
st.sidebar.title("🛠️ الأدوات الذكية")
choice = st.sidebar.selectbox("اختر الميزة التي تريدها:", 
    ["🌐 المترجم النصي", "📸 مترجم الصور (OCR)", "📝 ملخص النصوص", "💰 محول العملات", "🔍 فاحص الروابط"])

# --- 3. برمجة الميزات ---

# 🌐 المترجم النصي
if choice == "🌐 المترجم النصي":
    st.header("المترجم الفوري الشامل")
    text_input = st.text_area("أدخل النص المراد ترجمته إلى العربية:")
    if st.button("ترجم الآن"):
        if text_input:
            translated = GoogleTranslator(source='auto', target='ar').translate(text_input)
            st.success(translated)

# 📸 مترجم الصور
elif choice == "📸 مترجم الصور (OCR)":
    st.header("مترجم الصور الذكي")
    mode = st.radio("المصدر:", ["رفع ملف من المعرض", "استخدام الكاميرا"])
    img_file = st.file_uploader("اختر صورة") if mode == "رفع ملف من المعرض" else st.camera_input("التقط صورة")
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400)
        if st.button("قراءة النص وترجمته"):
            with st.spinner("جاري استخراج النص..."):
                reader = easyocr.Reader(['en', 'ar'])
                results = reader.readtext(np.array(img), detail=0)
                extracted_text = " ".join(results)
                st.write("**النص الأصلي:**", extracted_text)
                translated_img = GoogleTranslator(source='auto', target='ar').translate(extracted_text)
                st.success(f"**الترجمة:** {translated_img}")

# 📝 ملخص النصوص
elif choice == "📝 ملخص النصوص":
    st.header("ملخص النصوص الذكي")
    long_text = st.text_area("ضع النص الطويل هنا (بالعربية أو الإنجليزية):", height=200)
    if st.button("لخص"):
        if len(long_text) > 50:
            # محاكاة تلخيص (يمكن تطويرها لاحقاً باستخدام نماذج AI متقدمة)
            st.info("هذه الميزة ستقوم بتقليل النص لأهم النقاط الأساسية.")
            st.write(long_text[:len(long_text)//2] + "...") 
        else:
            st.warning("النص قصير جداً لتلخيصه!")

# 💰 محول العملات
elif choice == "💰 محول العملات":
    st.header("محول العملات المباشر")
    amount = st.number_input("المبلغ:", min_value=1.0)
    from_curr = st.text_input("من عملة (مثال: USD):", "USD").upper()
    to_curr = st.text_input("إلى عملة (مثال: SAR):", "SAR").upper()
    if st.button("تحويل"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url).json()
            rate = response['rates'][to_curr]
            result = amount * rate
            st.success(f"{amount} {from_curr} تساوي {result:.2 strangers} {to_curr}")
        except:
            st.error("تأكد من كتابة رموز العملات بشكل صحيح (مثل USD, EGP, SAR)")

# 🔍 فاحص الروابط
elif choice == "🔍 فاحص الروابط":
    st.header("فاحص أمان وسرعة الروابط")
    url_to_test = st.text_input("ضع الرابط هنا:")
    if st.button("فحص"):
        try:
            res = requests.get(url_to_test, timeout=5)
            st.success(f"الموقع متاح (Status Code: {res.status_code})")
        except:
            st.error("الموقع غير متاح أو الرابط غير صحيح.")
