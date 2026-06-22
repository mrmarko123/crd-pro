import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from analysis import run_full_analysis
from plots import box_plot, bar_plot, qq_plot

def render_results():
    """رندر نتایج تحلیل — بدون باکس خالی اضافی"""
    df = st.session_state.df

    st.markdown('<h2 class="crd-header" style="font-size: 2.8rem; margin-bottom: 1.5rem;">نتایج تحلیل CRD</h2>',
                unsafe_allow_html=True)

    with st.container():   # <-- جایگزین <div class="glass-container...">
        # اجرای تحلیل (با مدیریت خطا)
        try:
            results = run_full_analysis(df)
        except ValueError as e:
            st.warning(f"امکان اجرای ANOVA وجود ندارد: {e}")
            st.info("با این حال آمار توصیفی و نمودارها در ادامه نمایش داده می‌شوند.")
            results = {
                "p_value": None,
                "anova_table": pd.DataFrame(),
                "residuals": np.array([]),
                "p_shapiro": None,
                "p_levene": None,
                "assumption_status": "N/A",
                "posthoc": None
            }

        p_val = results["p_value"]
        anova_tab = results["anova_table"]
        residuals = results["residuals"]
        p_shapiro = results["p_shapiro"]
        p_levene = results["p_levene"]
        posthoc = results.get("posthoc")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 آمار توصیفی",
            "📈 ANOVA و پیش‌فرض‌ها",
            "🔬 مقایسه‌های چندگانه",
            "📉 visualizations",
            "📥 خروجی و گزارش"
        ])

        # ---------- تب ۱ ----------
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("تعداد مشاهدات", f"{len(df):,}")
            col2.metric("تعداد گروه‌ها", df['Treatment'].nunique())
            col3.metric("میانگین کل", f"{df['Value'].mean():.3f}")
            col4.metric("انحراف معیار کل", f"{df['Value'].std():.3f}")

            st.divider()
            st.subheader("آمار توصیفی گروهی")
            desc = df.groupby('Treatment')['Value'].describe().round(4)
            st.dataframe(
                desc.style.background_gradient(cmap='Blues', axis=0),
                use_container_width=True,
                height=420
            )

        # ---------- تب ۲ ----------
        with tab2:
            if p_val is not None:
                c1, c2 = st.columns([3, 1])
                c1.dataframe(anova_tab.round(5), use_container_width=True)
                if p_val < 0.05:
                    c2.success(f"**تفاوت معنی‌دار است**\np = {p_val:.5f}", icon="🎯")
                else:
                    c2.info(f"**تفاوت معنی‌دار نیست**\np = {p_val:.5f}", icon="ℹ️")

                st.divider()
                st.subheader("بررسی پیش‌فرض‌های ANOVA")
                ass_col1, ass_col2 = st.columns(2)
                ass_col1.metric("Shapiro-Wilk (نرمالیتی)", f"p = {p_shapiro:.4f}",
                                delta="✓ خوب" if p_shapiro > 0.05 else "⚠️ مشکوک")
                ass_col2.metric("Levene's Test (همگنی واریانس)", f"p = {p_levene:.4f}",
                                delta="✓ خوب" if p_levene > 0.05 else "⚠️ ناهمگن")
                if results["assumption_status"] == "Warning":
                    st.warning("⚠️ برخی پیش‌فرض‌ها نقض شده‌اند. نتایج را با احتیاط تفسیر کنید.")
            else:
                st.info("ANOVA به دلیل تعداد ناکافی گروه‌ها یا داده‌ها اجرا نشد. حداقل ۲ گروه برای تحلیل واریانس نیاز است.", icon="ℹ️")

        # ---------- تب ۳ ----------
        with tab3:
            if p_val is not None and p_val < 0.05 and posthoc and isinstance(posthoc, tuple):
                tukey_res, tukey_pvals, letter_df, method_name = posthoc
                st.subheader(f"نتایج آزمون {method_name}")
                st.text(tukey_res)
                col_t1, col_t2 = st.columns([1, 1])
                col_t1.subheader("ماتریس p-values")
                col_t1.dataframe(tukey_pvals.round(4).style.background_gradient(cmap='Reds_r'),
                                 use_container_width=True)
                col_t2.subheader("گروه‌بندی حروف معنی‌داری")
                col_t2.dataframe(letter_df.style.set_properties(**{'font-weight': 'bold'}),
                                 use_container_width=True)
            else:
                st.info("برای انجام مقایسه‌های چندگانه، ابتدا باید ANOVA معنی‌دار باشد (p < 0.05) و تعداد گروه‌ها بیشتر از ۲ باشد.", icon="ℹ️")

        # ---------- تب ۴ ----------
        with tab4:
            viz_col1, viz_col2 = st.columns(2)
            viz_col1.plotly_chart(box_plot(df), use_container_width=True)
            viz_col1.plotly_chart(bar_plot(df), use_container_width=True)
            if len(residuals) > 0:
                viz_col2.plotly_chart(qq_plot(residuals), use_container_width=True)
            else:
                viz_col2.info("برای نمایش Q-Q Plot نیاز به باقی‌مانده‌های مدل است (حداقل ۲ گروه).")

        # ---------- تب ۵ ----------
        with tab5:
            st.subheader("دانلود نتایج")
            dcol1, dcol2, dcol3 = st.columns(3)
            dcol1.download_button("📥 داده‌های خام (CSV)",
                                  df.to_csv(index=False).encode('utf-8'),
                                  f"CRD_Data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                                  mime="text/csv", use_container_width=True)
            try:
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Raw_Data', index=False)
                    desc.to_excel(writer, sheet_name='Descriptive_Stats')
                    if not anova_tab.empty:
                        anova_tab.to_excel(writer, sheet_name='ANOVA')
                dcol2.download_button("📊 گزارش کامل Excel", buf.getvalue(),
                                      f"CRD_Full_Report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                                      use_container_width=True)
            except Exception:
                dcol2.error("openpyxl نصب نیست.")
            dcol3.button("📄 گزارش PDF حرفه‌ای", use_container_width=True, disabled=True)

        st.divider()
        st.caption("تمام فایل‌ها با تاریخ و ساعت ذخیره می‌شوند.")

    st.markdown("""
    <div style="text-align:center; margin-top: 2.5rem; color: #64748b; font-size: 0.9rem;">
        CRD Pro — دقت علمی بالا • رابط کاربری لوکس
    </div>
    """, unsafe_allow_html=True)