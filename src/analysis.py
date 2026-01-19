"""
Analysis module for TB Global Analysis project.
Provides separate analysis pipelines for OWID and WHO data.
"""

import pandas as pd
import numpy as np

from logger import setup_logger
from config import TOP_N_COUNTRIES

logger = setup_logger(__name__)


# ============================================================================
# OWID-Specific Analysis (High-level trends, geographic patterns)
# ============================================================================

def owid_global_tb_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze global TB incidence trends over time using OWID data.
    
    Args:
        df: Cleaned OWID DataFrame
        
    Returns:
        DataFrame with global trends by year
    """
    logger.info("Calculating global TB trends from OWID data")
    
    # Select relevant columns - tb_incidence is our main metric
    if 'tb_incidence' not in df.columns:
        logger.warning("TB incidence column not found in OWID data")
        return pd.DataFrame()
    
    trends = (
        df.groupby('year')['tb_incidence']
        .mean()
        .reset_index()
        .rename(columns={'tb_incidence': 'avg_incidence'})
        .sort_values('year')
    )
    
    logger.info(f"Calculated trends for {len(trends)} years")
    return trends


def owid_top_affected_countries(df: pd.DataFrame, year: int = None, n: int = TOP_N_COUNTRIES) -> pd.DataFrame:
    """
    Identify most TB-affected countries in a given year using OWID data.
    
    Args:
        df: Cleaned OWID DataFrame
        year: Year to analyze (uses latest year if None)
        n: Number of top countries to return
        
    Returns:
        DataFrame with top countries ranked by TB burden
    """
    if df.empty:
        logger.warning("Cannot analyze empty OWID dataset")
        return pd.DataFrame()
    
    if year is None:
        year = int(df['year'].max())
    
    logger.info(f"Analyzing top {n} countries for year {year}")
    
    # Filter for target year
    year_data = df[df['year'] == year].copy()
    
    # Use TB incidence for ranking
    if 'tb_incidence' not in year_data.columns:
        logger.warning("TB incidence column not found")
        return pd.DataFrame()
    
    ranking_col = 'tb_incidence'
    
    top_countries = (
        year_data
        .dropna(subset=[ranking_col])
        .sort_values(ranking_col, ascending=False)
        .head(n)
        [['country', 'year', ranking_col]]
    )
    
    logger.info(f"Identified top {len(top_countries)} countries")
    return top_countries


def owid_country_incidence_trend(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Get TB incidence trend for a specific country from OWID data.
    
    Args:
        df: Cleaned OWID DataFrame
        country: Country name
        
    Returns:
        DataFrame with annual incidence for the country
    """
    country_data = df[df['country'] == country].copy()
    
    if country_data.empty:
        logger.warning(f"No data found for country: {country}")
        return pd.DataFrame()
    
    # Select incidence metric
    if 'tb_incidence' in country_data.columns:
        cols = ['country', 'year', 'tb_incidence']
    else:
        return pd.DataFrame()
    
    return country_data[cols].sort_values('year')


# ============================================================================
# WHO-Specific Analysis (Program performance, treatment outcomes)
# ============================================================================

def who_treatment_success_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze global TB treatment success rate trends using WHO data.
    
    Args:
        df: Cleaned WHO DataFrame
        
    Returns:
        DataFrame with treatment success trends by year
    """
    logger.info("Calculating TB treatment success trends from WHO data")
    
    if 'tb_treatment_success_rate' not in df.columns:
        logger.warning("TB treatment success rate not found in WHO data")
        return pd.DataFrame()
    
    trends = (
        df.groupby('year')['tb_treatment_success_rate']
        .mean()
        .reset_index()
        .rename(columns={'tb_treatment_success_rate': 'avg_treatment_success_rate'})
        .sort_values('year')
    )
    
    logger.info(f"Calculated treatment success trends for {len(trends)} years")
    return trends


def who_top_performers(df: pd.DataFrame, year: int = None, n: int = TOP_N_COUNTRIES) -> pd.DataFrame:
    """
    Identify countries with best TB treatment outcomes using WHO data.
    
    Args:
        df: Cleaned WHO DataFrame
        year: Year to analyze (uses latest year if None)
        n: Number of top countries to return
        
    Returns:
        DataFrame with top-performing countries
    """
    if df.empty:
        logger.warning("Cannot analyze empty WHO dataset")
        return pd.DataFrame()
    
    if year is None:
        year = df['year'].max()
    
    logger.info(f"Analyzing top {n} performing countries for year {year}")
    
    year_data = df[df['year'] == year].copy()
    
    if 'tb_treatment_success_rate' not in year_data.columns:
        logger.warning("Treatment success rate not available")
        return pd.DataFrame()
    
    top_performers = (
        year_data
        .dropna(subset=['tb_treatment_success_rate'])
        .sort_values('tb_treatment_success_rate', ascending=False)
        .head(n)
        [['country', 'year', 'tb_treatment_success_rate']]
    )
    
    logger.info(f"Identified {len(top_performers)} top-performing countries")
    return top_performers


def who_program_coverage_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze TB treatment coverage and case detection over time using WHO data.
    
    Args:
        df: Cleaned WHO DataFrame
        
    Returns:
        DataFrame with coverage indicators by year
    """
    logger.info("Analyzing TB program coverage from WHO data")
    
    coverage_metrics = []
    if 'tb_treatment_coverage' in df.columns:
        coverage_metrics.append('tb_treatment_coverage')
    if 'tb_cases_detected' in df.columns:
        coverage_metrics.append('tb_cases_detected')
    
    if not coverage_metrics:
        logger.warning("No coverage metrics found in WHO data")
        return pd.DataFrame()
    
    coverage = (
        df.groupby('year')[coverage_metrics]
        .mean()
        .reset_index()
        .sort_values('year')
    )
    
    logger.info(f"Calculated coverage metrics for {len(coverage)} years")
    return coverage


# ============================================================================
# Combined Analysis (Purposeful merging of OWID and WHO data)
# ============================================================================

def compare_incidence_vs_treatment_success(owid_df: pd.DataFrame, who_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare TB incidence against treatment success rates for insight.
    Merges OWID and WHO data purposefully to explore specific relationships.
    
    Args:
        owid_df: Cleaned OWID DataFrame
        who_df: Cleaned WHO DataFrame
        
    Returns:
        DataFrame with both metrics for countries/years where both exist
    """
    logger.info("Comparing TB incidence vs treatment success rates")
    
    # Prepare OWID data
    if 'tb_incidence' not in owid_df.columns:
        logger.warning("Incidence metric not available in OWID data")
        return pd.DataFrame()
    
    owid_subset = owid_df[['country', 'year', 'tb_incidence']].copy()
    
    # Prepare WHO data
    if 'tb_incidence' not in who_df.columns:
        logger.warning("No comparable metrics in WHO data for merging")
        return pd.DataFrame()
    
    who_subset = who_df[['country', 'year', 'tb_incidence']].copy()
    who_subset = who_subset.rename(columns={'tb_incidence': 'who_tb_incidence'})
    
    # Merge on country and year
    merged = pd.merge(
        owid_subset,
        who_subset,
        on=['country', 'year'],
        how='inner'
    )
    
    logger.info(f"Merged data: {len(merged)} country-year combinations")
    return merged.sort_values(['country', 'year'])
