import streamlit as st
import base64
import os

def get_font_base64(font_path="fonts/IRANSansRegular.ttf"):
    """بارگذاری فونت با مدیریت خطا"""
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def apply_professional_style():
    font_base64 = get_font_base64()
    
    st.set_page_config(
        page_title="CRD Pro | تحلیل طرح کاملاً تصادفی",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )

    font_css = f"""
    @font-face {{
        font-family: 'IranSans';
        src: url(data:font/truetype;base64,{font_base64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}""" if font_base64 else """
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
    """

    st.markdown(f"""
    <style>
        {font_css}

        /* فونت اصلی */
        * {{
            font-family: {'IranSans' if font_base64 else 'Vazirmatn'}, system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        /* ========= بمباران فضاهای خالی بالای صفحه ========= */
        /* حذف پدینگ و مارجین اضافی کانتینرهای اصلی */
        .main .block-container,
        .stApp .block-container,
        div[data-testid="stAppViewContainer"] > .block-container,
        section[data-testid="stAppViewContainer"] > div {{
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }}

        /* حذف کامل دکوریشن‌ها و نوار ابزارهای مخفی استریملیت */
        #MainMenu,
        footer,
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        .stDeployButton,
        .css-1dp5vir,
        .css-18ni7ap,
        .eyeqlp53 {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            pointer-events: none !important;
        }}

        /* استایل‌های جهانی لوکس */
        .stApp {{
            background: linear-gradient(135deg, #0a0a1f 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0f2fe;
        }}

        /* Glassmorphism Premium */
        .glass-container, .stContainer, div[data-testid="stExpander"] > div {{
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            padding: 2rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeIn 0.6s ease-out;          /* <-- اضافه شد */
        }}

        .glass-container:hover {{
            border-color: rgba(233, 69, 96, 0.5);
            box-shadow: 0 20px 50px rgba(233, 69, 96, 0.2);
            transform: translateY(-4px);
        }}

        /* هدر اصلی */
        .crd-header {{
            font-size: 3.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #e94560, #f39c12, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 1.5rem 0 0.5rem 0;
            letter-spacing: -2px;
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}

        @keyframes titleGlow {{
            from {{ filter: drop-shadow(0 0 20px #e94560); }}
            to {{ filter: drop-shadow(0 0 40px #4facfe); }}
        }}

        /* دکمه‌های حرفه‌ای */
        .stButton > button {{
            border-radius: 16px;
            height: 52px;
            font-weight: 700;
            font-size: 1.05rem;
            border: none;
            background: linear-gradient(90deg, #e94560, #f97316);
            color: white;
            box-shadow: 0 10px 30px rgba(233, 69, 96, 0.3);
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(233, 69, 96, 0.4);
        }}

        /* کارت‌های گروه */
        .group-card {{
            background: rgba(255,255,255,0.07);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 1.8rem;
            margin-bottom: 1.2rem;
        }}

        /* Data Editor */
        .stDataEditor {{
            border-radius: 16px;
            overflow: hidden;
        }}

        /* تب‌ها */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 12px 12px 0 0;
            padding: 12px 24px;
        }}

        /* متریک‌ها */
        [data-testid="stMetricValue"] {{
            font-size: 1.8rem;
            font-weight: 700;
        }}

        /* اسکرول بار لوکس */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #1a1a2e; }}
        ::-webkit-scrollbar-thumb {{ 
            background: linear-gradient(#e94560, #f39c12); 
            border-radius: 10px; 
        }}
    </style>
    """, unsafe_allow_html=True)