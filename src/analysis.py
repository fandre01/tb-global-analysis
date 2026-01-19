import pandas as pd

def global_tb_trends(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("year")
        .agg({
            "tb_deaths": "sum",
            "tb_incidence": "mean"
        })
        .reset_index()
    )

def top_affected_countries(df: pd.DataFrame, year: int, n=10):
    return (
        df[df["year"] == year]
        .sort_values("tb_incidence", ascending=False)
        .head(n)
    )
