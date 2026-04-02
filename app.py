import streamlit as st
import requests

st.title("🛡️ درع الفحص الأمني المطور")
url = st.text_input("ضع رابط الموقع هنا:")

if st.button("افحص الآن"):
    if url:
        try:
            if not url.startswith('http'): url = 'https://' + url
            # إضافة تعريف المتصفح لخداع أنظمة الحماية
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            r = requests.get(url, headers=headers, timeout=10)
            
            if r.status_code == 200:
                st.success(f"✅ الموقع يعمل بامتياز! الكود: {r.status_code}")
            else:
                st.warning(f"⚠️ الموقع رد بكود مختلف: {r.status_code}")
        except:
            st.error("❌ تعذر الوصول.. الموقع قد يكون محظوراً أو الرابط خاطئ.")
