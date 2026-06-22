import streamlit as st
import numpy as np
import pandas as pd

def render_input_section():
    """بخش ورود داده‌ها — روش تمیز بدون باکس خالی"""
    
    with st.container():   # <-- جایگزین <div class="glass-container...">
        st.markdown("""
        <h3 style="text-align:center; margin-bottom:1.5rem; color:#e0f2fe;">
            📥 ورود داده‌های آزمایشی
        </h3>
        """, unsafe_allow_html=True)

        # افزودن گروه جدید
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(
                "نام گروه جدید", 
                placeholder="مثال: کنترل، دوز ۱۰۰mg، تیمار A",
                key="new_group_input",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("➕ افزودن گروه", type="primary", use_container_width=True):
                name = new_name.strip()
                if name and name not in st.session_state.groups:
                    st.session_state.groups.append(name)
                    st.session_state.group_values[name] = ""
                    st.rerun()
                elif name:
                    st.warning("این گروه قبلاً وجود دارد", icon="⚠️")

        st.divider()

        if not st.session_state.groups:
            st.info("👈 حداقل یک گروه اضافه کنید.", icon="ℹ️")
        else:
            st.markdown("#### گروه‌های آزمایشی")

            for idx, g in enumerate(st.session_state.groups.copy()):
                with st.container():
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.05); border-radius:16px; padding:1.4rem; margin-bottom:1.2rem; 
                                border:1px solid rgba(233,69,96,0.3);">
                        <span style="color:#e94560; font-size:1.5rem;">●</span> 
                        <strong style="font-size:1.25rem;">{g}</strong>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns([6, 1])
                    with c1:
                        val = st.text_area(
                            label="مقادیر (جدا شده با کاما یا خط جدید)",
                            value=st.session_state.group_values.get(g, ""),
                            key=f"text_{g}_{idx}",
                            placeholder="23.5, 24.1, 22.8\n25.0 26.2 24.9",
                            height=140,
                            label_visibility="collapsed"
                        )
                        st.session_state.group_values[g] = val

                        if val and val.strip():
                            try:
                                parts = val.replace(',', ' ').replace('\n', ' ').split()
                                nums = [float(x) for x in parts if x.strip()]
                                if nums:
                                    preview_df = pd.DataFrame({"مقدار": nums})
                                    st.dataframe(
                                        preview_df.style.format("{:.4f}"),
                                        use_container_width=True,
                                        height=min(180, len(nums)*35 + 40),
                                        hide_index=True
                                    )
                                    st.success(f"✅ {len(nums)} مشاهده | میانگین: **{np.mean(nums):.3f}** | انحراف معیار: **{np.std(nums):.3f}**", 
                                             icon="📈")
                                else:
                                    st.warning("داده‌ای شناسایی نشد.")
                            except ValueError:
                                st.error("⚠️ فقط اعداد وارد کنید")
                        else:
                            st.info("داده‌ها را وارد کنید (کامپیوتر یا خط جدید)")

                    with c2:
                        if st.button("🗑️ حذف", key=f"del_{g}_{idx}", help="حذف گروه"):
                            st.session_state.groups.remove(g)
                            st.session_state.group_values.pop(g, None)
                            st.rerun()

            st.divider()

            valid_count = sum(
                len([x for x in st.session_state.group_values.get(g, "").replace(',', ' ').replace('\n', ' ').split() if x.strip()]) >= 1
                for g in st.session_state.groups
            )
            can_run = len(st.session_state.groups) >= 1 and valid_count == len(st.session_state.groups)

            if st.button(
                "🔍 اجرای تحلیل ANOVA",
                type="primary",
                use_container_width=True,
                disabled=not can_run
            ):
                parsed_data = {}
                for g in st.session_state.groups:
                    raw = st.session_state.group_values.get(g, "")
                    parts = raw.replace(',', ' ').replace('\n', ' ').split()
                    nums = [float(x) for x in parts if x.strip()]
                    parsed_data[g] = nums

                from analysis import build_dataframe
                df = build_dataframe(parsed_data)
                
                st.session_state.df = df
                st.session_state.run_analysis = True
                st.success(f"✅ تحلیل با {len(df)} مشاهده و {len(st.session_state.groups)} گروه شروع شد!", icon="🚀")
                st.rerun()