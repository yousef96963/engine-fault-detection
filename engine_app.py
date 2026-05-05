import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1. إعدادات واجهة غرفة التحكم الفخمة
st.set_page_config(page_title=" Maritime AI Control Center", page_icon="⚓", layout="wide")

# CSS لإضافة الخلفية وتنسيق العدادات اللي بتنور
st.markdown("""
    <style>
    .main {
        background-image: url("https://images.unsplash.com/photo-1544945582-3b466d3748cd?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp {
        background: rgba(0, 0, 0, 0.7); /* طبقة شفافة فوق الخلفية */
    }
    h1, h2, h3, p { color: #00d4ff !important; text-shadow: 0 0 5px #00d4ff; }
    
    /* تنسيق العدادات المربعة */
    .gauge-container {
        background-color: rgba(10, 15, 25, 0.8);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
        transition: all 0.3s ease;
    }
    .gauge-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.6);
    }
    .gauge-title {
        color: #fff;
        font-size: 20px;
        text-align: center;
        margin-bottom: 15px;
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    .gauge-value {
        font-size: 35px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الموديل الذكي (البيانات الشاملة لمنع اللخبطة)
@st.cache_resource
def train_engine_model():
    data = {
        'temp':      [70, 80, 85, 75, 120, 130, 80, 75, 80, 100], 
        'vibration': [0.01, 0.02, 0.02, 0.015, 0.05, 0.08, 0.02, 0.01, 0.02, 0.01],
        'pressure':  [50, 45, 48, 50, 20, 15, 45, 50, 45, 50],
        'rpm':       [1000, 1200, 1300, 1100, 2500, 2800, 1200, 1000, 1200, 1200],
        'status':    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0] # 0 سليم، 1 خطر
    }
    df = pd.DataFrame(data)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(df[['temp', 'vibration', 'pressure', 'rpm']], df['status'])
    return model

model = train_engine_model()

st.markdown("<h1 style='text-align: center;'>⚓ كشف اعطال المحرك</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. لوحة التحكم الجانبية (Sliders)
st.sidebar.header("🕹️ لوحة الحساسات")
temp = st.sidebar.slider("🌡️ درجة الحرارة (C°)", 60, 150, 80)
vib = st.sidebar.slider("📳 الاهتزاز (G)", 0.0, 0.1, 0.02, format="%.3f")
press = st.sidebar.slider("📊 ضغط الزيت (Bar)", 10, 60, 45)
rpm = st.sidebar.slider("⚙️ السرعة (RPM)", 500, 3000, 1200)

# 4. عرض العدادات الـ (Gauge Containers) في واجهة الصفحة
col1, col2, col3, col4 = st.columns(4)

# تحديد ألوان العدادات ديناميكياً
t_color = "#FF0000" if temp > 105 else "#00FF00"
v_color = "#FF0000" if vib > 0.045 else "#00FF00"
p_color = "#FF0000" if press < 30 else "#00FF00"
r_color = "#FF0000" if rpm > 2200 else "#00FF00"

with col1:
    st.markdown(f'<div class="gauge-container"><div class="gauge-title">🌡️ الحرارة</div><div class="gauge-value" style="color: {t_color};">{temp}°C</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="gauge-container"><div class="gauge-title">📳 الاهتزاز</div><div class="gauge-value" style="color: {v_color};">{vib:.3f}G</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="gauge-container"><div class="gauge-title">📊 الضغط</div><div class="gauge-value" style="color: {p_color};">{press} Bar</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="gauge-container"><div class="gauge-title">⚙️ السرعة</div><div class="gauge-value" style="color: {r_color};">{rpm} RPM</div></div>', unsafe_allow_html=True)

# 5. الفحص النهائي
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 تشغيل الفحص العميق"):
    prediction = model.predict([[temp, vib, press, rpm]])[0]
    
    # تحديد الأعطال الحقيقية بناءً على القواعد المنطقية
    real_issues = []
    if temp > 105: real_issues.append(f"❌ خطر: حرارة مرتفعة جداً ({temp}°C)")
    if vib > 0.045: real_issues.append(f"❌ خطر: اهتزاز غير آمن ({vib})")
    if press < 30: real_issues.append(f"❌ خطر: ضغط زيت منخفض ({press} Bar)")
    if rpm > 2200: real_issues.append(f"❌ خطر: سرعة زائدة ({rpm} RPM)")

    if len(real_issues) > 0:
        st.error("🚨 نتيجة الفحص: مطلوب صيانة فورية!")
        for issue in real_issues:
            st.warning(issue)
    else:
        st.success("✅ كافة الأنظمة تعمل بكفاءة تامة.")