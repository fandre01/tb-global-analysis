"""
Visualization module for TB Global Analysis project.
Creates static and interactive visualizations with proper figure management.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd

from logger import setup_logger
from config import FIGURES_DIR, MAPS_DIR, FIGURE_DPI, FIGURE_FORMAT, COLOR_PALETTE_TB, COLOR_PALETTE_TREATMENT

logger = setup_logger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def save_figure(fig, filename: str, output_dir: Path = FIGURES_DIR, dpi: int = FIGURE_DPI) -> None:
    """
    Save a matplotlib figure to disk.
    
    Args:
        fig: Matplotlib figure object
        filename: Name of file (without extension)
        output_dir: Directory to save figure
        dpi: Resolution in dots per inch
    """
    try:
        output_path = output_dir / f"{filename}.{FIGURE_FORMAT}"
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.info(f"Saved figure: {output_path}")
    except Exception as e:
        logger.error(f"Error saving figure {filename}: {e}")
        raise


def save_plotly_figure(fig, filename: str, output_dir: Path = FIGURES_DIR) -> None:
    """
    Save a Plotly figure to disk as HTML and static image.
    
    Args:
        fig: Plotly figure object
        filename: Name of file (without extension)
        output_dir: Directory to save figure
    """
    try:
        html_path = output_dir / f"{filename}.html"
        static_path = output_dir / f"{filename}.{FIGURE_FORMAT}"
        
        fig.write_html(html_path)
        logger.info(f"Saved interactive figure: {html_path}")
        
        # Try to save static image (requires kaleido)
        try:
            fig.write_image(static_path, width=1200, height=600)
            logger.info(f"Saved static figure: {static_path}")
        except Exception as e:
            logger.debug(f"Could not save static image (install kaleido if needed): {e}")
    except Exception as e:
        logger.error(f"Error saving Plotly figure {filename}: {e}")
        raise


# ============================================================================
# OWID Visualizations
# ============================================================================

def plot_global_tb_trends(df: pd.DataFrame, metric: str = 'tuberculosis_deaths') -> None:
    """
    Plot global TB trends over time using OWID data.
    
    Args:
        df: DataFrame with global trends by year
        metric: Column name to plot
    """
    logger.info(f"Creating global TB trends plot for {metric}")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if metric not in df.columns:
        logger.warning(f"Metric {metric} not found in data")
        return
    
    sns.lineplot(data=df, x='year', y=metric, marker='o', linewidth=2, ax=ax)
    
    ax.set_title('Global TB Trends Over Time (OWID Data)', fontsize=14, fontweight='bold')
    ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, f"global_tb_trends_{metric}")
    plt.close()


def plot_top_countries_comparison(df: pd.DataFrame, year: int, metric: str) -> None:
    """
    Create bar plot comparing TB burden across top countries.
    
    Args:
        df: DataFrame with top countries data
        year: Year displayed
        metric: Column name for comparison
    """
    logger.info(f"Creating top countries comparison plot for {year}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if metric not in df.columns:
        logger.warning(f"Metric {metric} not found")
        return
    
    sns.barplot(data=df, y='country', x=metric, ax=ax, palette='Reds_r')
    
    ax.set_title(f'Top Countries by TB Burden ({year})', fontsize=14, fontweight='bold')
    ax.set_xlabel(metric.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Country', fontsize=12)
    
    save_figure(fig, f"top_countries_tb_{year}")
    plt.close()


def plot_country_incidence_trend(df: pd.DataFrame, country: str) -> None:
    """
    Plot TB incidence trend for a specific country.
    
    Args:
        df: DataFrame with country-level annual data
        country: Country name to plot
    """
    logger.info(f"Creating incidence trend for {country}")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Find incidence column
    incidence_col = None
    for col in ['tuberculosis_incidence_rate', 'tuberculosis_incidence']:
        if col in df.columns:
            incidence_col = col
            break
    
    if incidence_col is None:
        logger.warning("No incidence column found")
        return
    
    sns.lineplot(data=df, x='year', y=incidence_col, marker='s', linewidth=2.5, ax=ax)
    
    ax.set_title(f'TB Incidence Trend: {country}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Incidence Rate', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    filename = f"incidence_trend_{country.lower().replace(' ', '_')}"
    save_figure(fig, filename)
    plt.close()


def animated_tb_map(df: pd.DataFrame, metric: str = 'tb_incidence') -> None:
    """
    Create animated choropleth map of TB spread over time using Plotly.
    
    Args:
        df: DataFrame with country, year, and metric columns
        metric: Column name for color scale
    """
    logger.info(f"Creating animated TB map for {metric}")
    
    if metric not in df.columns:
        logger.warning(f"Metric {metric} not found in data")
        return
    
    try:
        fig = px.choropleth(
            df,
            locations='country',
            locationmode='country names',
            color=metric,
            animation_frame='year',
            title=f'Global TB {metric.replace("_", " ").title()} Over Time',
            color_continuous_scale=COLOR_PALETTE_TB,
            range_color=[df[metric].min(), df[metric].quantile(0.95)],
            labels={metric: metric.replace('_', ' ')}
        )
        
        fig.update_layout(
            geo=dict(showframe=False),
            height=600,
            width=1200
        )
        
        save_plotly_figure(fig, f"animated_map_{metric}", MAPS_DIR)
        
    except Exception as e:
        logger.error(f"Error creating animated map: {e}")


# ============================================================================
# WHO Visualizations
# ============================================================================

def plot_treatment_success_trends(df: pd.DataFrame) -> None:
    """
    Plot TB treatment success rate trends over time.
    
    Args:
        df: DataFrame with treatment success trends by year
    """
    logger.info("Creating treatment success trends plot")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if 'avg_treatment_success_rate' not in df.columns:
        logger.warning("Treatment success rate column not found")
        return
    
    sns.lineplot(
        data=df,
        x='year',
        y='avg_treatment_success_rate',
        marker='o',
        linewidth=2.5,
        color='steelblue',
        ax=ax
    )
    
    ax.set_title('Global TB Treatment Success Rate Trends (WHO Data)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylim([0, 100])
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "treatment_success_trends")
    plt.close()


def plot_treatment_performers(df: pd.DataFrame, year: int) -> None:
    """
    Create bar plot of countries with best treatment outcomes.
    
    Args:
        df: DataFrame with treatment success rates by country
        year: Year displayed
    """
    logger.info(f"Creating treatment performer plot for {year}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'tb_treatment_success_rate' not in df.columns:
        logger.warning("Treatment success rate column not found")
        return
    
    sns.barplot(
        data=df,
        y='country',
        x='tb_treatment_success_rate',
        ax=ax,
        palette=COLOR_PALETTE_TREATMENT
    )
    
    ax.set_title(f'Top TB Treatment Performers ({year})', fontsize=14, fontweight='bold')
    ax.set_xlabel('Treatment Success Rate (%)', fontsize=12)
    ax.set_ylabel('Country', fontsize=12)
    ax.set_xlim([0, 100])
    
    save_figure(fig, f"treatment_performers_{year}")
    plt.close()


# ============================================================================
# Combined Analysis Visualizations
# ============================================================================

def plot_incidence_vs_treatment_scatter(df: pd.DataFrame) -> None:
    """
    Create scatter plot comparing TB incidence vs treatment success.
    
    Args:
        df: DataFrame with both metrics for country-year combinations
    """
    logger.info("Creating incidence vs treatment success scatter plot")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    required_cols = ['tuberculosis_incidence_rate', 'tb_treatment_success_rate']
    if not all(col in df.columns for col in required_cols):
        logger.warning("Required columns not found for scatter plot")
        return
    
    # Color by region if available, otherwise by year
    if 'region' in df.columns:
        scatter = ax.scatter(
            df['tuberculosis_incidence_rate'],
            df['tb_treatment_success_rate'],
            c=pd.Categorical(df['region']).codes,
            s=100,
            alpha=0.6,
            cmap='viridis'
        )
    else:
        scatter = ax.scatter(
            df['tuberculosis_incidence_rate'],
            df['tb_treatment_success_rate'],
            c=df['year'],
            s=100,
            alpha=0.6,
            cmap='RdYlGn'
        )
    
    ax.set_xlabel('TB Incidence Rate', fontsize=12)
    ax.set_ylabel('Treatment Success Rate (%)', fontsize=12)
    ax.set_title('TB Incidence vs Treatment Success Rate', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Year' if 'region' not in df.columns else 'Region')
    
    save_figure(fig, "incidence_vs_treatment")
    plt.close()
