import streamlit as st
import requests
import time
from deep_translator import GoogleTranslator

# إعداد القائمة الجانبية للتنقل
st.sidebar.title("🛠️ القائمة الرئيسية")
choice = st.sidebar.radio("اختر الأداة:", ["فاحص الروابط", "المترجم الفوري"])

if choice == "فاحص الروابط":
    st.header("🔍 فاحص الروابط الذكي")
    url = st.text_input("أدخل الرابط هنا:")
    if st.button("افحص"):
        # كود الفحص الذي كتبناه سابقاً
        st.write("جاري الفحص...")

elif choice == "المترجم الفوري":
    st.header("🌐 المترجم العالمي")
    text = st.text_area("اكتب النص المراد ترجمته إلى العربية:")
    if st.button("ترجم"):
        if text:
            # استخدام المكتبة للترجمة للعربية
            result = GoogleTranslator(source='auto', target='ar').translate(text)
            st.success(result)
        else:
            st.warning("الرجاء كتابة نص أولاً")
