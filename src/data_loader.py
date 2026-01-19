"""
Data loading module for TB Global Analysis project.
Handles loading OWID and WHO datasets with error handling and validation.
"""

import pandas as pd
from pathlib import Path

from logger import setup_logger

logger = setup_logger(__name__)


def load_owid_data(path: str) -> pd.DataFrame:
    """
    Load Our World in Data TB dataset.
    
    Args:
        path: Path to OWID TB CSV file
        
    Returns:
        DataFrame containing OWID TB data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or corrupted
    """
    try:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"OWID data file not found: {path}")
        
        logger.info(f"Loading OWID data from {path}")
        df = pd.read_csv(path)
        
        if df.empty:
            raise ValueError("OWID dataset is empty")
        
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns from OWID")
        logger.debug(f"OWID columns: {df.columns.tolist()}")
        
        return df
        
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error loading OWID data: {e}")
        raise


def load_who_data(path: str) -> pd.DataFrame:
    """
    Load World Health Organization TB dataset.
    
    Args:
        path: Path to WHO TB CSV file
        
    Returns:
        DataFrame containing WHO TB data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or corrupted
    """
    try:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"WHO data file not found: {path}")
        
        logger.info(f"Loading WHO data from {path}")
        df = pd.read_csv(path)
        
        if df.empty:
            raise ValueError("WHO dataset is empty")
        
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns from WHO")
        logger.debug(f"WHO columns: {df.columns.tolist()}")
        
        return df
        
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error loading WHO data: {e}")
        raise


def validate_dataframe(df: pd.DataFrame, name: str) -> None:
    """
    Validate a dataframe for basic data quality issues.
    
    Args:
        df: DataFrame to validate
        name: Name of dataset for logging
    """
    logger.info(f"Validating {name} dataset")
    
    # Check for completely empty columns
    empty_cols = df.columns[df.isna().all()].tolist()
    if empty_cols:
        logger.warning(f"{name}: Completely empty columns found: {empty_cols}")
    
    # Check for mostly missing data
    missing_pct = df.isna().sum() / len(df) * 100
    high_missing = missing_pct[missing_pct > 80]
    if not high_missing.empty:
        logger.warning(f"{name}: Columns with >80% missing data: {high_missing.to_dict()}")
    
    logger.info(f"{name} validation complete")
