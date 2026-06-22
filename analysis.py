"""
تحلیل آماری طرح کاملاً تصادفی (CRD)
نسخه حرفه‌ای - بهینه شده برای CRD Pro
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp
from typing import Tuple, Dict, Optional


def compact_letter_display(p_values: pd.DataFrame, alpha: float = 0.05) -> Dict[str, str]:
    """تولید حروف معنی‌داری با الگوریتم حریصانه دقیق"""
    groups = list(p_values.columns)
    n = len(groups)
    no_diff = p_values >= alpha
    letters = [''] * n
    used_letters = []

    for i in range(n):
        assigned = False
        for L in used_letters:
            if all(no_diff.iloc[i, j] for j in range(n) if letters[j] == L):
                letters[i] = L
                assigned = True
                break
        if not assigned:
            if used_letters:
                last = used_letters[-1]
                if last[-1] != 'z':
                    new_letter = last[:-1] + chr(ord(last[-1]) + 1) if len(last) == 1 else 'a' * (len(last) + 1)
                else:
                    new_letter = 'a' * (len(last) + 1)
            else:
                new_letter = 'a'
            letters[i] = new_letter
            used_letters.append(new_letter)

    return {grp: let for grp, let in zip(groups, letters)}


def build_dataframe(groups_data: dict) -> pd.DataFrame:
    """ساخت دیتافریم استاندارد از داده‌های ورودی (فیلتر مقادیر خالی)"""
    records = []
    for grp, vals in groups_data.items():
        for v in vals:
            if pd.notna(v) and str(v).strip() != '':
                records.append({'Treatment': str(grp), 'Value': float(v)})
    return pd.DataFrame(records)


def run_anova(df: pd.DataFrame) -> Tuple:
    """اجرای ANOVA یک‌طرفه. در صورت کمتر از دو گروه، ValueError صادر می‌کند."""
    if len(df['Treatment'].unique()) < 2:
        raise ValueError("برای انجام ANOVA حداقل به دو گروه نیاز است.")

    model = ols('Value ~ C(Treatment)', data=df).fit()
    anova_tab = anova_lm(model, typ=2)
    p_val = pd.to_numeric(anova_tab.loc['C(Treatment)', 'PR(>F)'])
    residuals = model.resid

    return model, anova_tab, p_val, residuals


def check_assumptions(df: pd.DataFrame, residuals: np.ndarray) -> Tuple[float, float, str]:
    """بررسی پیش‌فرض‌ها (Shapiro-Wilk و Levene)"""
    _, p_shapiro = stats.shapiro(residuals)
    groups = [df[df['Treatment'] == g]['Value'].values for g in df['Treatment'].unique()]
    _, p_levene = stats.levene(*groups)

    status = "Good"
    if p_shapiro < 0.05 or p_levene < 0.05:
        status = "Warning"

    return p_shapiro, p_levene, status


def run_posthoc(df: pd.DataFrame, method: str = "tukey") -> Tuple:
    """
    انجام مقایسه‌های چندگانه. در حال حاضر تنها Tukey HSD پشتیبانی می‌شود.
    """
    if method == "tukey":
        tukey_res = pairwise_tukeyhsd(df['Value'], df['Treatment'], alpha=0.05)
        tukey_pvals = sp.posthoc_tukey(df, val_col='Value', group_col='Treatment')

        letters = compact_letter_display(tukey_pvals)
        means = df.groupby('Treatment')['Value'].mean().round(4)

        letter_df = pd.DataFrame({
            'گروه': list(letters.keys()),
            'میانگین': [means[t] for t in letters.keys()],
            'حروف': list(letters.values())
        }).sort_values('میانگین', ascending=False)

        return tukey_res, tukey_pvals, letter_df, "Tukey HSD"

    else:
        raise ValueError(f"روش '{method}' پشتیبانی نمی‌شود. فعلاً فقط 'tukey' در دسترس است.")


def run_full_analysis(df: pd.DataFrame, posthoc_method: str = "tukey"):
    """
    تحلیل کامل: ANOVA، بررسی پیش‌فرض‌ها و در صورت نیاز Tukey HSD.
    """
    model, anova_tab, p_val, residuals = run_anova(df)
    p_shapiro, p_levene, assumption_status = check_assumptions(df, residuals)

    posthoc_results = None
    if p_val < 0.05 and len(df['Treatment'].unique()) > 2:
        try:
            posthoc_results = run_posthoc(df, method=posthoc_method)
        except Exception as e:
            posthoc_results = f"خطا در آزمون پس از آن: {e}"

    return {
        "model": model,
        "anova_table": anova_tab,
        "p_value": p_val,
        "residuals": residuals,
        "p_shapiro": p_shapiro,
        "p_levene": p_levene,
        "assumption_status": assumption_status,
        "posthoc": posthoc_results
    }