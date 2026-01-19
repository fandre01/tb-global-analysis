import pandas as pd

def clean_tb_data(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove rows without country or year
    df = df.dropna(subset=["country", "year"])

    # Convert year to integer
    df["year"] = df["year"].astype(int)

    # Forward fill missing values by country
    df = df.sort_values(["country", "year"])
    df = df.groupby("country").ffill()

    return df
