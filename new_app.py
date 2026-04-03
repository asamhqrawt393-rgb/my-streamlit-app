import streamlit as st
import requests
from deep_translator import GoogleTranslator

# --- 1. إعدادات الصفحة والتصميم (CSS) ---
st.set_page_config(page_title="منصة أسامة الذكية", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: white;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }
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
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(37, 117, 252, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظائف جلب البيانات ---
@st.cache_data(ttl=3600)
def get_rates():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        return requests.get(url).json()['rates']
    except:
        return {"USD": 1, "SAR": 3.75, "EGP": 48}

all_rates = get_rates()

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.title("🛡️ نظام أسامة الذكي")
    choice = st.selectbox("اختر الأداة:", [
        "💰 محول العملات العالمي",
        "✍️ المترجم النصي",
        "🔍 فاحص الأمان",
        "📱 كاشف الأرقام"
    ])
    st.write("---")
    st.info("👤 المطور: أسامة قراوط")

# --- 4. تنفيذ الأدوات ---

# أداة 1: محول العملات
if choice == "💰 محول العملات العالمي":
    st.markdown("<div class='glass-card'><h2>💰 محول العملات العالمي</h2></div>", unsafe_allow_html=True)
    currency_list = sorted(list(all_rates.keys()))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: amount = st.number_input("المبلغ:", min_value=0.01, value=1.0)
    with col2: from_c = st.selectbox("من:", currency_list, index=currency_list.index("USD"))
    with col3: to_c = st.selectbox("إلى:", currency_list, index=currency_list.index("SAR"))
    
    if st.button("احسب الآن ✨"):
        res = amount * (all_rates[to_c] / all_rates[from_c])
        st.success(f"النتيجة: {res:.2f} {to_c}")

# أداة 2: المترجم
elif choice == "✍️ المترجم النصي":
    st.markdown("<div class='glass-card'><h2>✍️ المترجم الذكي</h2></div>", unsafe_allow_html=True)
    translator = GoogleTranslator()
    all_langs = translator.get_supported_languages(as_dict=True)
    
    text = st.text_area("أدخل النص:")
    c1, c2 = st.columns(2)
    with c1: src_l = st.selectbox("من لغة:", ["auto"] + list(all_langs.keys()))
    with c2: tgt_l = st.selectbox("إلى لغة:", list(all_langs.keys()), index=list(all_langs.keys()).index('english'))
    
    if st.button("ترجمة الآن ✨"):
        if text:
            s = src_l if src_l == "auto" else all_langs[src_l]
            t = all_langs[tgt_l]
            result = GoogleTranslator(source=s, target=t).translate(text)
            st.markdown("### ✅ النتيجة:")
            st.text_area("انسخ من هنا:", value=result, height=150)

# أداة 3: فاحص الأمان
elif choice == "🔍 فاحص الأمان":
    st.markdown("<div class='glass-card'><h2>🔍 فاحص الروابط والملفات</h2></div>", unsafe_allow_html=True)
    url_in = st.text_input("افحص رابطاً:")
    if url_in:
        if not url_in.startswith("https://") or any(w in url_in.lower() for w in ["login", "free"]):
            st.error("⚠️ تحذير: الرابط قد يكون غير آمن!")
        else: st.success("✅ يبدو آمناً.")
    
    file = st.file_uploader("افحص ملفاً:", type=['pdf', 'png', 'jpg', 'zip'])
    if file is not None:
        size = file.size / (1024*1024)
        if size > 10: st.warning(f"⚠️ الملف كبير ({size:.2f}MB)")
        else: st.success("✅ حجم الملف مناسب.")

# أداة 4: كاشف الأرقام
elif choice == "📱 كاشف الأرقام":
    st.markdown("<div class='glass-card'><h2>📱 كاشف مفاتيح الدول</h2></div>", unsafe_allow_html=True)
    codes = {"967": "اليمن 🇾🇪", "966": "السعودية 🇸🇦", "20": "مصر 🇪🇬", "971": "الإمارات 🇦🇪"}
    num = st.text_input("أدخل الرقم الدولي:")
    if num:
        clean = num.replace("+", "").lstrip("0")
        for length in [3, 2]:
            if clean[:length] in codes:
                st.success(f"📍 الدولة: {codes[clean[:length]]}")
                break
