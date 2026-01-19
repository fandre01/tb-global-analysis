# Global Tuberculosis Trends Analysis

This project analyzes global tuberculosis trends using WHO and Our World in Data datasets.
It focuses on data tidying, large-scale CSV handling, and visualization.

## Tools
- Python
- Pandas
- Plotly
- Matplotlib
- VS Code

## Key Skills Demonstrated
- Data cleaning and restructuring
- Public health data analysis
- Geospatial visualization
- Reproducible data science workflows

## Quick start
1. Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. Expected input columns (after cleaning): `country`, `year`, `tb_deaths`, `tb_incidence`, `population` (optional)

3. Example usage from Python:

```python
from src.data_loader import load_owid_data
from src.data_cleaning import clean_tb_data
from src.analysis import global_tb_trends
from src.visualization import plot_global_trends

raw = load_owid_data('data/raw/owid_tb.csv')
df = clean_tb_data(raw)
trends = global_tb_trends(df)
plot_global_trends(trends, value_col='tb_deaths')
```
