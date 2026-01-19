# Updated: support Path-like paths, read options, docstrings
from pathlib import Path
from typing import Union, Optional, Dict
import pandas as pd


def load_csv(path: Union[str, Path], read_csv_kwargs: Optional[Dict] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    path : str | Path
        Local filesystem path or URL to CSV.
    read_csv_kwargs : dict, optional
        Extra kwargs forwarded to pandas.read_csv (e.g., parse_dates, dtype, compression).

    Returns
    -------
    pd.DataFrame
    """
    read_csv_kwargs = read_csv_kwargs or {}
    path = Path(path) if not isinstance(path, str) else path
    try:
        df = pd.read_csv(path, **read_csv_kwargs)
    except Exception:
        # Try letting pandas handle URL strings if path is a URL string
        df = pd.read_csv(path, **read_csv_kwargs)
    return df


def load_owid_data(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """Load Our World In Data style CSV (wrapper over load_csv)."""
    return load_csv(path, read_csv_kwargs=kwargs)


def load_who_data(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """Load WHO dataset CSV (wrapper over load_csv)."""
    return load_csv(path, read_csv_kwargs=kwargs)
