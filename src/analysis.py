# Updated: added docstrings, validation, typing
from typing import Optional
import pandas as pd


def global_tb_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate global TB trends by year.

    Returns a DataFrame with columns: year, tb_deaths (sum), tb_incidence (mean)

    Raises if required columns are missing.
    """
    required = {"year", "tb_deaths", "tb_incidence"}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    return (
        df.groupby("year", as_index=False)
        .agg({"tb_deaths": "sum", "tb_incidence": "mean"})
        .reset_index(drop=True)
    )


def top_affected_countries(df: pd.DataFrame, year: int, n: int = 10, incidence_col: str = "tb_incidence") -> pd.DataFrame:
    """
    Return top `n` countries by incidence for a given year.

    Parameters
    ----------
    df : pd.DataFrame
    year : int
    n : int
    incidence_col : str
        Column to sort by (default 'tb_incidence')

    Returns
    -------
    pd.DataFrame
    """
    if "year" not in df.columns:
        raise ValueError("DataFrame must contain 'year' column")
    if incidence_col not in df.columns:
        raise ValueError(f"DataFrame must contain '{incidence_col}' column")

    sub = df[df["year"] == year]
    return sub.sort_values(incidence_col, ascending=False).head(n)
