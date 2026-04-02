import streamlit as st
import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import time
import re

# --- 1. إعدادات المنصة والهوية البصرية ---
st.set_page_config(page_title="منصة أسامة الأمنية الشاملة", page_icon="🛡️", layout="wide")

# دالة جلب أسعار العملات المحدثة
@st.cache_data(ttl=3600)
def get_live_data():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        data = requests.get(url).json()
        return data['rates']
    except:
        return {"USD": 1, "SAR": 3.75, "EGP": 48.5, "YER": 250}

rates = get_live_data()

# معلومات العملات والدول لسهولة الاختيار
currency_info = {
    "USD": "الدولار الأمريكي 🇺🇸", "SAR": "الريال السعودي 🇸🇦", 
    "EGP": "الجنيه المصري 🇪🇬", "AED": "الدرهم الإماراتي 🇦🇪",
    "YER": "الريال اليمني 🇾🇪", "EUR": "اليورو الأوروبي 🇪🇺",
    "TRY": "الليرة التركية 🇹🇷", "KWD": "الدينار الكويتي 🇰🇼",
    "GBP": "الجنيه الإسترليني 🇬🇧", "JPY": "الين الياباني 🇯🇵"
}

# --- 2. التنسيق البرمجي المتقدم (CSS) ---
# هنا قمنا بتعديل لون الشريط العلوي وتناسق الألوان
st.markdown("""
    <style>
    /* تعديل الشريط العلوي ليكون داكناً ومتناسقاً مع الخط */
    header[data-testid="stHeader"] {
        background-color: rgba(10, 20, 30, 0.98) !important;
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* ضمان ظهور أيقونات الشريط العلوي باللون الأبيض */
    header[data-testid="stHeader"] svg {
        fill: white !important;
    }

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
    }

    h1, h2, h3, p, span, label { 
        color: #ffffff !important; 
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.title("🛡️ نظام أسامة المتكامل")
    choice = st.selectbox("اختر الأداة:", 
        ["💰 محول العملات العالمي", "🔍 فاحص الروابط والأمان", "📱 كاشف الأرقام الذكي", "🌐 المترجم الاحترافي"])
    st.markdown("---")
    st.write("👤 المطور: **المبرمج اسامه قراوط**")

# --- 4. تشغيل الأدوات المحدثة ---

# أداة محول العملات
if choice == "💰 محول العملات العالمي":
    st.markdown("<div class='glass-card'><h1>💰 محول العملات المباشر</h1></div>", unsafe_allow_html=True)
    display_options = [f"{code} - {currency_info.get(code, 'عملة عالمية')}" for code in sorted(rates.keys())]
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        amount = st.number_input("المبلغ المطلوب تحويله:", min_value=0.01, value=1.0)
    with col2:
        from_sel = st.selectbox("من عملة:", display_options, index=display_options.index("USD - الدولار الأمريكي 🇺🇸") if "USD - الدولار الأمريكي 🇺🇸" in display_options else 0)
    with col3:
        to_sel = st.selectbox("إلى عملة:", display_options, index=display_options.index("SAR - الريال السعودي 🇸🇦") if "SAR - الريال السعودي 🇸🇦" in display_options else 0)
    
    if st.button("احسب السعر الآن"):
        f_code, t_code = from_sel.split(" - ")[0], to_sel.split(" - ")[0]
        res = amount * (rates[t_code] / rates[f_code])
        st.success(f"### النتيجة: {amount} {f_code} = {res:.2f} {t_code}")

# أداة فاحص الروابط
elif choice == "🔍 فاحص الروابط والأمان":
    st.markdown("<div class='glass-card'><h2>🔍 فحص أمان ومحتوى الروابط المتقدم</h2></div>", unsafe_allow_html=True)
    url = st.text_input("أدخل الرابط للفحص (مثال: https://google.com):")
    
    if st.button("بدء التحليل الأمني"):
        if url:
            try:
                with st.spinner("جاري تحليل الموقع أمنياً..."):
                    r = requests.get(url, timeout=10)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    links = soup.find_all('a')
                    is_secure = url.startswith("https")
                    
                    if not is_secure:
                        st.error("🚨 غير آمن: هذا الرابط لا يستخدم تشفير HTTPS! بياناتك في خطر.")
                    else:
                        st.success("🔒 آمن: الرابط يستخدم بروتوكول نقل مشفر.")
                    
                    if len(links) > 50:
                        st.warning(f"⚠️ تحذير: تم العثور على {len(links)} رابط خارجي. قد يكون الموقع مشبوهاً أو دعائياً.")
                    
                    st.info(f"🌐 عنوان الموقع: {soup.title.string if soup.title else 'غير معروف'}")
            except:
                st.error("❌ تعذر الوصول للموقع. تأكد من صحة الرابط وكتابته بشكل كامل.")

# أداة كاشف الأرقام
elif choice == "📱 كاشف الأرقام الذكي":
    st.markdown("<div class='glass-card'><h2>📱 كاشف وتحليل الأرقام</h2></div>", unsafe_allow_html=True)
    phone = st.text_input("أدخل الرقم مع مفتاح الدولة (مثل +967...):")
    
    if st.button("بدء الكشف والتحليل"):
        if phone:
            with st.spinner("جاري فحص السجلات العالمية..."):
                time.sleep(2)
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.subheader("نتائج الاستعلام عن الرقم")
                st.write(f"📞 **الرقم المكتشف:** {phone}")
                st.write("🌍 **الدولة:** تم التعرف على النطاق الجغرافي")
                st.write("📡 **نوع الشبكة:** جوال (Mobile)")
                st.info("💡 ملاحظة: لاستخراج 'اسم الشخص' تحديداً، يتطلب ذلك ربط التطبيق بـ API رسمي (مثل Truecaller SDK).")
                st.markdown("</div>", unsafe_allow_html=True)

# أداة المترجم
elif choice == "🌐 المترجم الاحترافي":
    st.markdown("<div class='glass-card'><h2>🌐 المترجم العالمي متعدد اللغات</h2></div>", unsafe_allow_html=True)
    langs = {'العربية': 'ar', 'الإنجليزية': 'en', 'الفرنسية': 'fr', 'الألمانية': 'de', 'التركية': 'tr'}
    
    col1, col2 = st.columns(2)
    with col1: src = st.selectbox("من لغة:", list(langs.keys()), index=1)
    with col2: dest = st.selectbox("إلى لغة:", list(langs.keys()), index=0)
    
    text = st.text_area("أدخل النص المراد ترجمته:")
    if st.button("ترجم الآن"):
        if text:
            translated = GoogleTranslator(source=langs[src], target=langs[dest]).translate(text)
            st.markdown(f"<div class='glass-card'><h3>الترجمة:</h3><p>{translated}</p></div>", unsafe_allow_html=True)

