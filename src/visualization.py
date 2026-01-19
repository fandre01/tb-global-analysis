# Updated: return figures, add save options, docstrings, use ISO if provided
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd


def plot_global_trends(df: pd.DataFrame, value_col: str = "tb_deaths", show: bool = True, save_path: Optional[str] = None):
    """
    Plot global trends over time for a given column.

    Returns matplotlib.Figure for further use.
    """
    if "year" not in df.columns or value_col not in df.columns:
        raise ValueError("DataFrame must contain 'year' and the requested value column")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x="year", y=value_col, ax=ax)
    ax.set_title(f"Global {value_col} Over Time")
    ax.set_ylabel(value_col)
    ax.set_xlabel("Year")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def animated_tb_map(df: pd.DataFrame, country_col: str = "country", value_col: str = "tb_incidence", year_col: str = "year", iso_col: Optional[str] = None, save_html: Optional[str] = None):
    """
    Create an animated choropleth showing TB incidence over time.

    If `iso_col` is provided, it will be used with locationmode='ISO-3'.
    Otherwise function uses country names and locationmode='country names' (less reliable).

    Returns plotly.graph_objs.Figure
    """
    if year_col not in df.columns or value_col not in df.columns or country_col not in df.columns:
        raise ValueError(f"Expected columns: {year_col}, {value_col}, {country_col}")

    if iso_col and iso_col in df.columns:
        locations = iso_col
        locationmode = "ISO-3"
    else:
        locations = country_col
        locationmode = "country names"

    fig = px.choropleth(
        df,
        locations=locations,
        locationmode=locationmode,
        color=value_col,
        animation_frame=year_col,
        title="Global TB Incidence Over Time",
        color_continuous_scale="Reds",
    )
    if save_html:
        fig.write_html(save_html)
    fig.show()
    return fig
