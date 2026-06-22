import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

def update_plot_style(fig, title: str = "", height: int = 520):
    """استایل مشترک حرفه‌ای برای همه نمودارها"""
    fig.update_layout(
        title=dict(
            text=title,
            font_size=20,
            font_color="#e0f2fe",
            x=0.5,
            xanchor="center"
        ),
        height=height,
        margin=dict(l=50, r=30, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="IranSans, Vazirmatn, sans-serif", color="#cbd5e1"),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.7)",
            bordercolor="rgba(233, 69, 96, 0.3)",
            borderwidth=1,
            font_size=14,
        ),
        hovermode="closest",
        template="plotly_dark",
    )
    
    # Grid و محورها
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor="rgba(148, 163, 184, 0.2)",
        zeroline=False,
        title_font_size=15
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor="rgba(148, 163, 184, 0.2)",
        zeroline=False,
        title_font_size=15
    )
    return fig


def box_plot(df):
    fig = px.box(
        df, 
        x="Treatment", 
        y="Value", 
        color="Treatment",
        points="all",
        notched=True,                    # برای نمایش CI
        template="plotly_dark"
    )
    
    fig.update_traces(
        marker=dict(size=6, opacity=0.7),
        line=dict(width=2.5),
        fillcolor="rgba(233, 69, 96, 0.25)"
    )
    
    fig = update_plot_style(fig, "📦 Box Plot + Individual Points", height=560)
    return fig


def bar_plot(df):
    means = df.groupby('Treatment')['Value'].agg(['mean', 'std', 'count']).reset_index()
    means['se'] = means['std'] / np.sqrt(means['count'])   # Standard Error
    
    fig = px.bar(
        means, 
        x="Treatment", 
        y="mean", 
        color="Treatment",
        error_y="se",
        text=means['mean'].apply(lambda x: f'{x:.3f}'),
        template="plotly_dark"
    )
    
    fig.update_traces(
        textposition='outside',
        marker_line_color='white',
        marker_line_width=1.5
    )
    
    fig = update_plot_style(fig, "📊 میانگین هر تیمار ± خطای استاندارد", height=520)
    return fig


def qq_plot(residuals):
    # محاسبه QQ Plot دستی برای کنترل بیشتر
    sorted_res = np.sort(residuals)
    n = len(sorted_res)
    theor = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
    
    fig = go.Figure()
    
    # نقاط
    fig.add_trace(go.Scatter(
        x=theor, y=sorted_res,
        mode='markers',
        name='Residuals',
        marker=dict(color='#4facfe', size=8, opacity=0.85)
    ))
    
    # خط مرجع نرمال
    min_val = min(theor.min(), sorted_res.min())
    max_val = max(theor.max(), sorted_res.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='خط نرمال',
        line=dict(color='#e94560', dash='dash', width=2.5)
    ))
    
    fig = update_plot_style(fig, "🔍 Q-Q Plot (نرمالیتی residuals)", height=520)
    fig.update_layout(
        xaxis_title="Theoretical Quantiles",
        yaxis_title="Sample Quantiles"
    )
    return fig