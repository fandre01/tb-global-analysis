# Updated: more robust cleaning, docstrings, typing, safe numeric coercion
from typing import List, Optional
import pandas as pd


def clean_tb_data(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Clean a tuberculosis dataset.

    - Normalizes column names (strip, lower, replace spaces with underscores)
    - Converts `year` to integer (nullable integer type) after coercion
    - Drops rows missing country or year
    - Sorts by country/year and forward/backward fills within each country
    - Coerces common numeric columns to numeric dtype

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe to clean (will be copied; input not modified).
    required_columns : Optional[List[str]]
        If provided, function will raise a ValueError when any of these columns are missing.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Rename 'entity' to 'country' if present (common in OWID datasets)
    if "entity" in df.columns and "country" not in df.columns:
        df = df.rename(columns={"entity": "country"})

    # Optional: validate required columns early
    if required_columns:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    # Coerce year to numeric then to nullable integer type
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    else:
        raise ValueError("Expected column 'year' in the dataframe")

    # Drop rows without country or year
    if "country" not in df.columns:
        raise ValueError("Expected column 'country' in the dataframe")
    df = df.dropna(subset=["country", "year"])

    # Ensure proper sorting before fill
    df = df.sort_values(["country", "year"])

    # Forward + backward fill within each country to impute missing data sensibly
    # Use transform to avoid the FutureWarning from apply
    for col in df.columns:
        if col not in ["country", "year"]:
            df[col] = df.groupby("country")[col].transform(lambda x: x.ffill().bfill())

    # Coerce commonly used numeric columns if they exist
    numeric_cols = ["tb_deaths", "tb_incidence", "population", "cases"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
