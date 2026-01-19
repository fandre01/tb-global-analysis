# Quick Start Guide - TB Global Analysis

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Ensure Data Files Exist
- Place `tb_owid.csv` in `data/raw/`
- Place `tb_who.csv` in `data/raw/`

### Step 3: Run the Pipeline
```bash
python src/pipeline.py
```

That's it! The complete analysis will execute automatically.

---

## 📊 What Happens Next

The pipeline will:
1. ✅ Load OWID and WHO datasets
2. ✅ Clean and standardize the data
3. ✅ Perform OWID analysis (TB trends)
4. ✅ Perform WHO analysis (Program performance)
5. ✅ Combine datasets for insights
6. ✅ Generate visualizations
7. ✅ Save cleaned data and figures
8. ✅ Log all steps with timestamps

**Duration:** Typically 1-2 minutes depending on dataset size

---

## 📁 Where to Find Results

After running the pipeline:

| Output | Location |
|--------|----------|
| Cleaned OWID data | `data/processed/tb_owid_cleaned.csv` |
| Cleaned WHO data | `data/processed/tb_who_cleaned.csv` |
| Merged dataset | `data/processed/tb_merged.csv` |
| TB trend plots | `outputs/figures/` |
| Performance plots | `outputs/figures/` |
| Execution log | `logs/tb_analysis.log` |

---

## 🎯 Alternative Execution Methods

### Interactive Jupyter Notebook
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```
Run cells one-by-one to explore the data step-by-step.

### Custom Analysis Script
```python
from src.pipeline import TBAnalysisPipeline

pipeline = TBAnalysisPipeline()
pipeline.load_data()
pipeline.clean_data()
pipeline.analyze_owid()    # Just OWID analysis
```

### Direct Function Usage
```python
from src.data_loader import load_owid_data, load_who_data
from src.data_cleaning import clean_owid_data, clean_who_data
from src.analysis import owid_global_tb_trends

owid = load_owid_data('data/raw/tb_owid.csv')
owid_clean = clean_owid_data(owid)
trends = owid_global_tb_trends(owid_clean)
```

---

## 🔧 Customize the Analysis

Edit `src/config.py` to change:
- **Analysis years:** `MIN_YEAR`, `MAX_YEAR`
- **Top countries:** `TOP_N_COUNTRIES`
- **Visualization DPI:** `FIGURE_DPI`
- **Color scheme:** `COLOR_PALETTE_TB`
- **Logging level:** `LOG_LEVEL`

Example:
```python
# src/config.py
MIN_YEAR = 2000        # Analyze from 2000 onward
MAX_YEAR = 2022        # Up to 2022
TOP_N_COUNTRIES = 15   # Show top 15 instead of 10
FIGURE_DPI = 600       # Higher resolution figures
```

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "No such file or directory" Error
Make sure `data/raw/tb_owid.csv` and `data/raw/tb_who.csv` exist

### Output directories not created
Directories are auto-created. If issues persist, run:
```bash
mkdir -p data/processed outputs/figures outputs/maps logs
```

### Want to see detailed logs?
```bash
cat logs/tb_analysis.log
```

---

## 📊 Understanding the Output

### Cleaned Data Files
- Columns standardized to lowercase with underscores
- Missing values handled appropriately
- Duplicates removed
- Data filtered to relevant year range
- Ready for analysis and modeling

### Visualizations
- **PNG files:** Static images suitable for reports and presentations
- **HTML files:** Interactive plots for exploration

### Log File
Shows every step of execution with timestamps:
```
2026-01-18 14:32:15 - Data loading successful
2026-01-18 14:32:16 - Starting general cleaning for owid data
2026-01-18 14:32:17 - OWID-specific cleaning complete: 1234 rows remaining
```

---

## 📚 Learn More

- Full documentation: See `README.md`
- Project improvements: See `PROJECT_IMPROVEMENTS.md`
- Code details: Check docstrings in each Python file
- Example analysis: Run `notebooks/exploratory_analysis.ipynb`

---

## ✨ Key Project Structure

```
src/
├── config.py          ← Customize here
├── pipeline.py        ← Run this: python src/pipeline.py
├── data_loader.py     ← Loads raw data
├── data_cleaning.py   ← Cleans data
├── analysis.py        ← Performs analysis
└── visualization.py   ← Creates plots
```

---

## 🎉 You're Ready!

Your TB Global Analysis project is fully set up and ready to use. Run the pipeline, explore the data, and generate insights about global TB trends!

**Questions?** Check the README.md or view the Jupyter notebook for detailed examples.
