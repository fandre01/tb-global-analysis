import pandas as pd

def load_owid_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_who_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
