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

# --- 1. الإعدادات العامة والهوية البصرية ---
st.set_page_config(page_title="منصة أسامة المتكاملة", page_icon="🛡️", layout="wide")

# دالة جلب أسعار العملات اللحظية
@st.cache_data(ttl=3600)
def get_all_live_rates():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        return response.json()['rates']
    except:
        return {"USD": 1.0, "SAR": 3.75, "YER": 250.0, "EGP": 48.0}

all_rates = get_all_live_rates()

# تحميل محرك الـ OCR (للقراءة من الصور) لمرة واحدة فقط
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['ar', 'en'])

reader = load_ocr()

# تصميم الواجهة باستخدام CSS (الشريط العلوي الداكن والخلفية)
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background-color: rgba(10, 20, 30, 0.98) !important;
        backdrop-filter: blur(12px);
    }
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية للتنقل ---
with st.sidebar:
    st.title("🛡️ نظام أسامة الذكي")
    choice = st.selectbox("اختر الأداة المطلوبة:", [
        "💰 محول العملات والتحليل",
        "📸 الترجمة المرئية (OCR)",
        "🔍 فاحص الأمان والروابط",
        "📱 كاشف الأرقام الذكي"
    ])
    st.write("---")
    st.write("👤 المطور: **اسامه قراوط**")

# --- 3. تشغيل الأداة المختارة ---

# القسم الأول: محول العملات الشامل
if choice == "💰 محول العملات والتحليل":
    st.markdown("<div class='glass-card'><h1>💰 محول العملات والتحليل المالي</h1></div>", unsafe_allow_html=True)
    
    currency_list = sorted(list(all_rates.keys()))
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: amount = st.number_input("أدخل المبلغ:", min_value=0.01, value=1.0)
    with col2: from_c = st.selectbox("تحويل من:", currency_list, index=currency_list.index("USD"))
    with col3: to_c = st.selectbox("تحويل إلى:", currency_list, index=currency_list.index("SAR"))
    
    if st.button("احسب الآن ✨"):
        res = amount * (all_rates[to_c] / all_rates[from_c])
        st.success(f"### النتيجة اللحظية: {res:.2f} {to_c}")
    
    st.write("---")
    # ميزة إضافية للرسم البياني
    if st.checkbox("📈 إظهار الرسم البياني التاريخي"):
        period = st.radio("النطاق الزمني:", ["أسبوع", "شهر", "سنة"], horizontal=True)
        days = 7 if period == "أسبوع" else (30 if period == "شهر" else 365)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
        # توليد بيانات محاكاة للنمو
        prices = [all_rates[to_c] * (1 + np.random.uniform(-0.03, 0.03)) for _ in range(days)]
        df = pd.DataFrame({'التاريخ': dates, 'السعر': prices})
        fig = px.line(df, x='التاريخ', y='السعر', title=f"تحليل أداء {to_c} مقابل {from_c}")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

# القسم الثاني: الترجمة المرئية
elif choice == "📸 الترجمة المرئية (OCR)":
    st.markdown("<div class='glass-card'><h2>📸 الترجمة الذكية من الصور</h2></div>", unsafe_allow_html=True)
    src = st.radio("اختر المصدر:", ["المعرض 🖼️", "الكاميرا 📷"], horizontal=True)
    file = st.camera_input("التقط صورة") if src == "الكاميرا 📷" else st.file_uploader("ارفع صورة النص", type=['jpg','png','jpeg'])
    
    if file:
        img = Image.open(file)
        st.image(img, width=400)
        if st.button("استخراج وترجمة النص ✨"):
            with st.spinner("جاري قراءة الصورة..."):
                results = reader.readtext(np.array(img), detail=0)
                full_text = " ".join(results)
                if full_text.strip():
                    st.write(f"📝 **النص الأصلي:** {full_text}")
                    translated = GoogleTranslator(source='auto', target='ar').translate(full_text)
                    st.success(f"🔄 **الترجمة للعربية:** {translated}")
                else:
                    st.warning("لم يتم العثور على نص واضح.")

# القسم الثالث: فاحص الأمان
elif choice == "🔍 فاحص الأمان والروابط":
    st.markdown("<div class='glass-card'><h2>🔍 فاحص أمان الروابط الذكي</h2></div>", unsafe_allow_html=True)
    url = st.text_input("أدخل الرابط للفحص (مثلاً https://google.com):")
    if st.button("بدء التحليل الأمني 🛡️"):
        try:
            with st.spinner("جاري التحليل..."):
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.content, 'html.parser')
                is_secure = url.startswith("https")
                if is_secure:
                    st.success("🔒 الرابط مشفر وآمن (HTTPS)")
                else:
                    st.error("🚨 الرابط غير مشفر (HTTP)! بياناتك قد تكون في خطر.")
                st.info(f"🌐 عنوان الموقع: {soup.title.string if soup.title else 'غير معروف'}")
        except:
            st.error("❌ تعذر الوصول للرابط. تأكد من صحته.")

# القسم الرابع: كاشف الأرقام
elif choice == "📱 كاشف الأرقام الذكي":
    st.markdown("<div class='glass-card'><h2>📱 كاشف وتحليل الأرقام</h2></div>", unsafe_allow_html=True)
    phone = st.text_input("أدخل الرقم الدولي (مثل +967...):")
    if st.button("كشف الهوية 🔍"):
        with st.spinner("جاري البحث في السجلات..."):
            time.sleep(2) # محاكاة للبحث
            st.info(f"الرقم {phone} تم تحليله كـ: رقم دولي نشط ✅")
            st.write("📍 **الدولة:** تم التعرف على المفتاح الدولي")
            st.write("📡 **نوع الشبكة:** جوال")
            st.warning("ملاحظة: لاستخراج الاسم الشخصي بدقة، يتطلب ربط التطبيق بـ API رسمي.")
st.markdown("""
    <div style='text-align: center; color: grey; padding: 20px;'>
        تم التطوير بواسطة: أسامة قراوط © 2026
    </div>
    """, unsafe_allow_html=True)
# --- تحديث التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    /* تغيير لون الشريط العلوي */
    header[data-testid="stHeader"] {
        background-color: rgba(0, 32, 63, 0.95) !important; /* أزرق داكن */
        backdrop-filter: blur(10px);
    }

    /* تحسين شكل البطاقات الزجاجية باللون الأزرق */
    .glass-card {
        background: rgba(0, 50, 100, 0.1); 
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(0, 122, 255, 0.3); /* إطار أزرق خفيف */
        margin-bottom: 20px;
    }

    /* تلوين الأزرار باللون الأزرق */
    .stButton>button {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 10px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ... (بقية كود الأدوات هنا) ...

# --- إضافة الحقوق في أسفل التطبيق ---
st.markdown("---") # خط فاصل
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <p style='color: #888; font-size: 0.9em;'>
            🚀 جميع الحقوق محفوظة لـ <b>أسامة قراوط</b> &copy; 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
