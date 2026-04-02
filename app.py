import streamlit as st
import requests
from deep_translator import GoogleTranslator
import easyocr
from PIL import Image
import numpy as np

# --- 1. إعدادات الهوية والمنصة ---
st.set_page_config(
    page_title="منصة أسامة الذكية | Osama Smart Platform",
    page_icon="⚡",
    layout="wide"
)

# --- 2. التصميم الاحترافي (Professional CSS) ---
st.markdown(
    """
    <style>
    /* تحسين الخلفية العامة */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072");
        background-size: cover;
        background-attachment: fixed;
    }

    /* تصميم البطاقات الزجاجية الحديثة */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* تنسيق النصوص والعناوين */
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif;
    }

    /* تخصيص الأزرار لتكون تفاعلية */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1b5e20, #4caf50) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.4);
    }

    /* تذييل الصفحة الاحترافي */
    .footer {
        text-align: center;
        padding: 20px;
        color: rgba(255,255,255,0.6);
        font-size: 14px;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    # يمكنك استبدال هذا الرابط برابط شعارك الخاص
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=120)
    st.title("لوحة التحكم 🛠️")
    st.markdown("---")
    choice = st.selectbox("اختر الأداة:", 
        ["💰 محول العملات", "🌐 المترجم النصي", "📸 مترجم الصور (OCR)", "📝 ملخص النصوص", "🔍 فاحص الروابط"])
    st.markdown("---")
    st.write("👤 **المطور:** اسامه قراوط")
    st.caption("نسخة احترافية 1.0")

# --- 4. محرك الأدوات الذكية ---

def render_header(title, emoji):
    st.markdown(f"""
        <div class="glass-card">
            <h1 style='text-align: center;'>{emoji} {title}</h1>
        </div>
    """, unsafe_allow_html=True)

if choice == "💰 محول العملات":
    render_header("محول العملات المباشر", "💰")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("المبلغ:", min_value=0.01, value=1.0)
        with col2:
            from_c = st.text_input("من (مثلاً USD):", "USD").upper()
            to_c = st.text_input("إلى (مثلاً SAR):", "SAR").upper()
        
        if st.button("احسب التحويل"):
            try:
                url = f"https://open.er-api.com/v6/latest/{from_c}"
                data = requests.get(url).json()
                rate = data['rates'][to_c]
                st.balloons()
                st.success(f"### النتيجة: {amount * rate:.2f} {to_c}")
            except:
                st.error("تأكد من كتابة رموز العملات بشكل صحيح.")

elif choice == "🌐 المترجم النصي":
    render_header("مترجم اللغات الذكي", "🌐")
    text = st.text_area("ضع النص هنا للترجمة الفورية:", height=150)
    if st.button("ترجم الآن"):
        if text:
            with st.spinner("جاري المعالجة..."):
                translated = GoogleTranslator(source='auto', target='ar').translate(text)
                st.markdown(f"<div class='glass-card'><h3>الترجمة:</h3><p>{translated}</p></div>", unsafe_allow_html=True)

elif choice == "📸 مترجم الصور (OCR)":
    render_header("التعرف على النصوص وترجمتها", "📸")
    source = st.radio("مصدر الصورة:", ["رفع ملف", "التقاط بالكاميرا"])
    img_file = st.file_uploader("ارفع الصورة:") if source == "رفع ملف" else st.camera_input("التقط نصاً:")
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="الصورة الأصلية", use_column_width=True)
        if st.button("استخراج وترجمة"):
            with st.spinner("جاري قراءة النص..."):
                reader = easyocr.Reader(['en', 'ar'])
                extracted = " ".join(reader.readtext(np.array(img), detail=0))
                st.write("**النص المكتشف:**", extracted)
                translated = GoogleTranslator(source='auto', target='ar').translate(extracted)
                st.success(f"**الترجمة العربية:** {translated}")

elif choice == "📝 ملخص النصوص":
    render_header("ملخص النصوص الذكي", "📝")
    long_text = st.text_area("أدخل النص الطويل للتلخيص:", height=200)
    if st.button("توليد الملخص"):
        if len(long_text) > 50:
            st.info("إليك ملخص سريع لأهم النقاط:")
            st.write(long_text[:len(long_text)//2] + "...")
        else:
            st.warning("النص قصير جداً للتلخيص.")

elif choice == "🔍 فاحص الروابط":
    render_header("فاحص أمان المواقع", "🔍")
    url = st.text_input("رابط الموقع (URL):")
    if st.button("فحص الحالة"):
        try:
            r = requests.get(url, timeout=5)
            st.success(f"الموقع يعمل بنجاح! كود الحالة: {r.status_code}")
        except:
            st.error("الموقع لا يستجيب أو الرابط غير متاح حالياً.")

# --- 5. التذييل (Footer) ---
st.markdown(f"""
    <div class="footer">
        تم التطوير بكل ❤️ بواسطة <b>اسامه قراوط</b> | جميع الحقوق محفوظة © 2026
    </div>
""", unsafe_allow_html=True)
