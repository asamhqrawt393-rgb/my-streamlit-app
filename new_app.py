import streamlit as st
import requests
from deep_translator import GoogleTranslator

# --- 1. إعدادات الصفحة والتصميم المتطور (CSS) ---
st.set_page_config(page_title="منصة أسامة الذكية", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: white;
    }
    
    /* البطاقة الزجاجية للعناوين */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }

    /* تلوين القوائم المنسدلة باللون الأزرق */
    div[data-baseweb="select"] > div {
        background-color: #2575fc !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* الأزرار بنمط متدرج */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0px 4px 15px rgba(37, 117, 252, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. دالة جلب أسعار العملات ---
@st.cache_data(ttl=3600)
def get_live_rates():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        return requests.get(url).json()['rates']
    except:
        return {"USD": 1, "SAR": 3.75, "YER": 250, "EGP": 48}

all_rates = get_live_rates()

# --- 3. القائمة الجانبية للتنقل ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ نظام أسامة الذكي</h2>", unsafe_allow_html=True)
    choice = st.selectbox("قائمة الأدوات:", [
        "💰 محول العملات العالمي",
        "✍️ المترجم النصي الشامل",
        "🔍 فاحص الأمان الذكي",
        "📱 كاشف أرقام الدول"
    ])
    st.write("---")
    st.info("👤 المطور: أسامة قراوط")

# --- 4. منطق الأدوات ---

if choice == "💰 محول العملات العالمي":
    st.markdown("<div class='glass-card'><h2>💰 محول العملات العالمي</h2></div>", unsafe_allow_html=True)
    currencies = sorted(list(all_rates.keys()))
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: amount = st.number_input("المبلغ:", min_value=0.01, value=1.0)
    with col2: from_val = st.selectbox("من:", currencies, index=currencies.index("USD"))
    with col3: to_val = st.selectbox("إلى:", currencies, index=currencies.index("SAR"))
    if st.button("تحويل الآن ✨"):
        result = amount * (all_rates[to_val] / all_rates[from_val])
        st.success(f"### النتيجة: {result:.2f} {to_val}")

elif choice == "✍️ المترجم النصي الشامل":
    st.markdown("<div class='glass-card'><h2>✍️ المترجم الذكي</h2></div>", unsafe_allow_html=True)
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    text = st.text_area("أدخل النص المراد ترجمته:")
    c1, c2 = st.columns(2)
    with c1: src = st.selectbox("من لغة:", ["auto"] + list(langs.keys()))
    with c2: tgt = st.selectbox("إلى لغة:", list(langs.keys()), index=list(langs.keys()).index('english'))
    if st.button("ترجمة"):
        if text:
            s_code = src if src == "auto" else langs[src]
            res = GoogleTranslator(source=s_code, target=langs[tgt]).translate(text)
            st.text_area("النتيجة (قابلة للنسخ):", value=res, height=150)

elif choice == "🔍 فاحص الأمان الذكي":
    st.markdown("<div class='glass-card'><h2>🔍 فاحص الروابط والملفات</h2></div>", unsafe_allow_html=True)
    url = st.text_input("ضع الرابط هنا لفحصه:")
    if url:
        if not url.startswith("https://") or "login" in url.lower():
            st.error("⚠️ تحذير: هذا الرابط قد يكون غير آمن!")
        else: st.success("✅ الرابط يبدو آمناً.")
    
    file = st.file_uploader("ارفع ملفاً لفحص الحجم:", type=['pdf', 'png', 'jpg', 'zip'])
    if file:
        size_mb = file.size / (1024*1024)
        if size_mb > 10: st.warning(f"⚠️ حجم الملف كبير جداً ({size_mb:.2f} MB)")
        else: st.success("✅ حجم الملف سليم.")

elif choice == "📱 كاشف أرقام الدول":
    st.markdown("<div class='glass-card'><h2>📱 كاشف مفاتيح الدول</h2></div>", unsafe_allow_html=True)
    codes = {"967": "اليمن 🇾🇪", "966": "السعودية 🇸🇦", "20": "مصر 🇪🇬", "971": "الإمارات 🇦🇪", "44": "بريطانيا 🇬🇧", "1": "أمريكا 🇺🇸"}
    num = st.text_input("أدخل الرقم (بدأً بمفتاح الدولة):")
    if num:
        clean = num.replace("+", "").lstrip("0")
        found = False
        for i in [3, 2, 1]:
            if clean[:i] in codes:
                st.success(f"📍 هذا الرقم يتبع: **{codes[clean[:i]]}**")
                found = True; break
        if not found: st.warning("المفتاح غير مسجل في قاعدة بياناتنا حالياً.")

# --- 5. ذيل الصفحة (حقوق المطور) ---
st.markdown("""
    <br><hr style="border:0.5px solid rgba(255,255,255,0.1)">
    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 10px; font-size: 0.9em;">
        جميع الحقوق محفوظة © 2026 | تم التطوير بواسطة <b>أسامة قراوط</b> 🚀
    </div>
    """, unsafe_allow_html=True)
