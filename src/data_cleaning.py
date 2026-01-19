"""
Data cleaning module for TB Global Analysis project.
Handles standardization, validation, and tidying of OWID and WHO datasets.
"""

import pandas as pd
import numpy as np

from logger import setup_logger
from config import MIN_YEAR, MAX_YEAR

logger = setup_logger(__name__)


def clean_tb_data(df: pd.DataFrame, source: str = "generic") -> pd.DataFrame:
    """
    Apply general cleaning to TB datasets.
    
    Args:
        df: Raw DataFrame to clean
        source: Data source identifier ("owid", "who", or "generic")
        
    Returns:
        Cleaned DataFrame
    """
    logger.info(f"Starting general cleaning for {source} data")
    df = df.copy()
    
    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    logger.debug(f"Standardized columns: {df.columns.tolist()}")
    
    # Remove completely duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
    
    # Handle missing values in key columns
    key_cols = ['country', 'year']
    if all(col in df.columns for col in key_cols):
        df = df.dropna(subset=key_cols)
        logger.info(f"Removed rows with missing country or year: {initial_rows - len(df)} rows")
    
    # Convert year to integer if present
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        df = df.dropna(subset=['year'])
        
        # Filter to valid year range
        initial_rows = len(df)
        df = df[(df['year'] >= MIN_YEAR) & (df['year'] <= MAX_YEAR)]
        logger.info(f"Filtered to years {MIN_YEAR}-{MAX_YEAR}: {initial_rows - len(df)} rows removed")
    
    # Sort by country and year for forward fill
    if 'country' in df.columns and 'year' in df.columns:
        df = df.sort_values(['country', 'year']).reset_index(drop=True)
    
    logger.info(f"General cleaning complete: {len(df)} rows remaining")
    return df


def clean_owid_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply OWID-specific cleaning and standardization.
    Focuses on TB incidence, mortality, and epidemiological indicators.
    
    Args:
        df: Raw OWID DataFrame
        
    Returns:
        Cleaned OWID DataFrame
    """
    logger.info("Starting OWID-specific cleaning")
    df = df.copy()
    
    # Rename columns to standard names
    if 'Entity' in df.columns:
        df = df.rename(columns={'Entity': 'country'})
    if 'Year' in df.columns:
        df = df.rename(columns={'Year': 'year'})
    if 'Estimated incidence of all forms of tuberculosis' in df.columns:
        df = df.rename(columns={'Estimated incidence of all forms of tuberculosis': 'tb_incidence'})
    
    df = clean_tb_data(df, source="owid")
    
    # Common OWID TB columns (after renaming)
    tb_indicators = [
        'tb_incidence',
        'tuberculosis_deaths',
        'tuberculosis_incidence_rate',
        'tuberculous_mortality_rate',
        'population'
    ]
    
    # Forward fill missing values by country (for time series continuity)
    if 'country' in df.columns:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df.groupby('country')[col].transform(lambda x: x.ffill())
        logger.debug("Applied forward fill to numeric columns grouped by country")
    
    # Remove rows where all TB indicators are missing
    available_indicators = [col for col in tb_indicators if col in df.columns]
    if available_indicators:
        df = df.dropna(subset=available_indicators, how='all')
        logger.info(f"Removed rows with all TB indicators missing: {len(df)} rows remaining")
    
    logger.info("OWID-specific cleaning complete")
    return df


def clean_who_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply WHO-specific cleaning and standardization.
    Focuses on TB cases, treatment outcomes, and program indicators.
    
    Args:
        df: Raw WHO DataFrame
        
    Returns:
        Cleaned WHO DataFrame
    """
    logger.info("Starting WHO-specific cleaning")
    df = df.copy()
    
    # Rename columns to standard names
    if 'Entity' in df.columns:
        df = df.rename(columns={'Entity': 'country'})
    if 'Year' in df.columns:
        df = df.rename(columns={'Year': 'year'})
    if 'Estimated incidence of all forms of tuberculosis' in df.columns:
        df = df.rename(columns={'Estimated incidence of all forms of tuberculosis': 'tb_incidence'})
    
    df = clean_tb_data(df, source="who")
    
    # Common WHO TB program indicators
    who_indicators = [
        'tb_cases_notified',
        'tb_treatment_success_rate',
        'tb_treatment_coverage',
        'tb_cases_detected',
        'tb_cases_with_drug_susceptibility_test'
    ]
    
    # Handle percentage columns (treatment success rate typically 0-100)
    percentage_cols = [col for col in df.columns if 'success_rate' in col or 'coverage' in col]
    for col in percentage_cols:
        if col in df.columns:
            # Ensure percentages are in 0-100 range
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df.loc[df[col] > 100, col] = np.nan
            logger.debug(f"Standardized percentage column: {col}")
    
    # Forward fill missing values by country
    if 'country' in df.columns:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df.groupby('country')[col].transform(lambda x: x.ffill())
    
    # Remove rows where all indicators are missing
    available_indicators = [col for col in who_indicators if col in df.columns]
    if available_indicators:
        df = df.dropna(subset=available_indicators, how='all')
        logger.info(f"Removed rows with all WHO indicators missing: {len(df)} rows remaining")
    
    logger.info("WHO-specific cleaning complete")
    return df


def identify_outliers(df: pd.DataFrame, columns: list, zscore_threshold: float = 3) -> pd.DataFrame:
    """
    Identify potential outliers using z-score method.
    
    Args:
        df: DataFrame to analyze
        columns: Columns to check for outliers
        zscore_threshold: Z-score threshold for outlier detection
        
    Returns:
        DataFrame with outlier flag
    """
    from scipy import stats
    
    df = df.copy()
    df['is_outlier'] = False
    
    for col in columns:
        if col in df.columns:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers = z_scores > zscore_threshold
            df.loc[outliers.index, 'is_outlier'] = True
    
    outlier_count = df['is_outlier'].sum()
    logger.info(f"Identified {outlier_count} potential outliers")
    
    return df
