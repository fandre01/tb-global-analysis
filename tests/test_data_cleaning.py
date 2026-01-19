import pandas as pd
from src.data_cleaning import clean_tb_data


def test_clean_tb_data_basic():
    raw = pd.DataFrame({
        'Country': ['A', 'A', 'B'],
        'Year': [2000, '2001', 2000],
        'tb_deaths': [10, None, 5],
        'tb_incidence': [100, 110, None]
    })

    out = clean_tb_data(raw)
    assert 'country' in out.columns
    assert out['year'].dtype.name.startswith('Int')
    assert not out[['country', 'year']].isnull().any().any()
