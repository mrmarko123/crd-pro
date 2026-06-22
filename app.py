"""
CRD Pro — پلتفرم حرفه‌ای تحلیل طرح کاملاً تصادفی
نسخه: 3.0
"""

import streamlit as st
from style import apply_professional_style
from session_init import init_session
from ui_input import render_input_section
from ui_results import render_results

# اعمال استایل (شامل set_page_config و CSS)
apply_professional_style()

# مقداردهی اولیه session_state
init_session()

# ====================== HEADER ======================
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <h1 class="crd-header animate-fade-in">🧬 CRD PRO</h1>
        <p style="color: #94a3b8; font-size: 1.35rem; margin-top: 0.5rem;">
            تحلیل پیشرفته طرح کاملاً تصادفی (One-Way ANOVA)
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ====================== MAIN CONTENT ======================
# پیام خوش‌آمدگویی فقط زمانی که هنوز تحلیلی انجام نشده و گروهی اضافه نشده است
if not st.session_state.get("run_analysis", False) and len(st.session_state.get("groups", [])) == 0:
    st.markdown("""
    <div class="glass-container" style="text-align:center; padding:3rem 2rem;">
        <h3 style="color:#cbd5e1;">👋 خوش آمدید به CRD Pro</h3>
        <p style="color:#94a3b8; max-width:600px; margin:0 auto;">
            گروه‌های آزمایشی خود را تعریف کنید، داده‌ها را وارد نمایید 
            و تحلیل کامل ANOVA، مقایسه‌های چندگانه و visualization حرفه‌ای را مشاهده کنید.
        </p>
    </div>
    """, unsafe_allow_html=True)

# بخش ورودی داده‌ها (همیشه نمایش داده شود)
render_input_section()

# بخش نتایج تحلیل
if (
    st.session_state.get("run_analysis", False) 
    and "df" in st.session_state 
    and not st.session_state.df.empty
):
    render_results()

# ====================== FOOTER ======================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.95rem; padding: 1.5rem 0;">
        CRD Pro v3.0 — ساخته شده برای محققان و دانشجویان ایرانی با استانداردهای جهانی<br>
        <span style="font-size: 0.85rem;">دقت علمی • رابط کاربری لوکس • تجربه کاربری روان</span>
    </div>
    """, 
    unsafe_allow_html=True
)