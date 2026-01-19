# Global Tuberculosis Trends Analysis

A professional Python data science project analyzing global tuberculosis (TB) trends using public health data from Our World in Data (OWID) and the World Health Organization (WHO). This project demonstrates industry-standard workflows for data loading, cleaning, analysis, and visualization.

## 📋 Project Overview

This project transforms raw, messy epidemiological datasets into clean, standardized formats to examine long-term TB incidence and mortality patterns, compare countries over time, and assess key program indicators such as treatment success rates.

**Key Objectives:**
- Analyze OWID data for high-level TB trends and geographic patterns
- Analyze WHO data for TB program performance indicators
- Perform targeted merging to explore relationships between TB incidence and treatment success
- Create professional visualizations communicating meaningful insights

## 📊 Analysis Strategy

1. **OWID Data Analysis** (Incidence & Mortality Trends)
   - Global TB death and incidence trends over time
   - Top affected countries by burden
   - Country-level temporal patterns
   - Geographic distribution of TB

2. **WHO Data Analysis** (Program Performance)
   - TB treatment success rate trends
   - Top-performing countries by treatment outcomes
   - TB program coverage indicators
   - Case detection rates and other metrics

3. **Combined Analysis** (Targeted Merging)
   - TB incidence vs treatment success relationships
   - Correlation analysis between burden and program performance
   - Insight-driven comparative visualizations

## 📁 Project Structure

```
tb-global-analysis/
├── data/
│   ├── raw/                          # Source datasets
│   │   ├── tb_owid.csv              # OWID TB data
│   │   └── tb_who.csv               # WHO TB data
│   ├── processed/                    # Cleaned datasets
│   │   ├── tb_owid_cleaned.csv
│   │   ├── tb_who_cleaned.csv
│   │   └── tb_merged.csv
│   └── readme.md
├── src/                              # Python source code
│   ├── config.py                    # Configuration and paths
│   ├── logger.py                    # Logging utility
│   ├── data_loader.py               # Data loading with validation
│   ├── data_cleaning.py             # Data cleaning pipelines
│   ├── analysis.py                  # OWID/WHO/combined analysis
│   ├── visualization.py             # Plot generation and saving
│   └── pipeline.py                  # Main orchestration script
├── notebooks/
│   └── exploratory_analysis.ipynb    # Interactive analysis notebook
├── outputs/
│   ├── figures/                      # Generated visualizations
│   └── maps/                         # Geospatial visualizations
├── logs/                             # Application logs
├── README.md                         # This file
├── .gitignore
└── requirements.txt                  # Python dependencies
```

## 🛠️ Technologies & Tools

- **Language:** Python 3.8+
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Geospatial:** GeoPandas, Pycountry
- **Jupyter:** Interactive notebook analysis
- **Version Control:** Git
- **IDE:** Visual Studio Code

## 📦 Installation & Setup

### 1. Clone or Download the Repository
```bash
cd tb-global-analysis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Running the Project

### Option 1: Run Full Pipeline
```bash
python src/pipeline.py
```

This executes the complete workflow:
- Loads raw OWID and WHO data
- Cleans and standardizes datasets
- Performs OWID-specific analysis
- Performs WHO-specific analysis
- Combines data for targeted analysis
- Generates all visualizations

### Option 2: Interactive Jupyter Notebook
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

This allows step-by-step exploration with detailed output and visualizations.

### Option 3: Custom Analysis
Import modules in your own Python script:
```python
from src.config import OWID_DATA_PATH, WHO_DATA_PATH
from src.data_loader import load_owid_data, load_who_data
from src.data_cleaning import clean_owid_data, clean_who_data
from src.analysis import owid_global_tb_trends, who_treatment_success_trends
from src.visualization import plot_global_tb_trends, plot_treatment_success_trends

# Load and clean
owid = clean_owid_data(load_owid_data(str(OWID_DATA_PATH)))
who = clean_who_data(load_who_data(str(WHO_DATA_PATH)))

# Analyze
trends = owid_global_tb_trends(owid)
success = who_treatment_success_trends(who)

# Visualize
plot_global_tb_trends(trends)
plot_treatment_success_trends(success)
```

## 📊 Generated Outputs

### Visualizations
- **global_tb_trends_tuberculosis_deaths.png** - Global TB death trends over time
- **top_countries_tb_[YEAR].png** - Top affected countries bar chart
- **treatment_success_trends.png** - Global treatment success trends
- **treatment_performers_[YEAR].png** - Top-performing countries
- **incidence_vs_treatment.png** - Scatter plot of incidence vs success rates
- **incidence_trend_[COUNTRY].png** - Country-level temporal patterns

### Datasets
- **tb_owid_cleaned.csv** - Cleaned OWID dataset
- **tb_who_cleaned.csv** - Cleaned WHO dataset
- **tb_merged.csv** - Combined OWID/WHO dataset for incidence-treatment analysis

### Logs
- **logs/tb_analysis.log** - Detailed execution logs with timestamps

## 🔑 Key Features

✅ **Professional Workflows**
- Modular code structure with separation of concerns
- Comprehensive error handling and logging
- Configuration management for easy customization
- Reproducible analysis pipeline

✅ **Data Quality**
- Automatic validation and outlier detection
- Missing value handling strategies
- Data standardization and normalization
- Source-specific cleaning protocols

✅ **Analysis Capabilities**
- OWID-specific trend analysis
- WHO-specific program performance analysis
- Targeted dataset merging
- Correlation and comparative analysis

✅ **Visualization Suite**
- Static plots (PNG, high-resolution)
- Interactive plots (HTML, Plotly)
- Multiple visualization types (line, bar, scatter, choropleth)
- Figure saving and management

## 📈 Key Metrics Analyzed

### OWID
- TB incidence rates
- TB mortality rates
- Deaths per 100,000 population
- Geographic distribution

### WHO
- Treatment success rates (%)
- Case detection rates
- Treatment coverage
- Drug susceptibility testing rates

### Combined
- Incidence vs treatment success correlations
- Program performance vs burden relationships
- Country comparison insights

## 🔄 Data Processing Pipeline

1. **Load** → Raw data from OWID and WHO CSV files
2. **Validate** → Check for completeness and integrity
3. **Clean** → Standardize columns, handle missing values, remove duplicates
4. **Tidy** → Convert to long format, ensure consistency
5. **Analyze** → Apply source-specific analysis functions
6. **Merge** → Purposefully combine for targeted insights
7. **Visualize** → Generate static and interactive plots
8. **Save** → Export cleaned data, figures, and logs

## 📝 Configuration

Edit `src/config.py` to customize:
- Data paths and directories
- Analysis parameters (year ranges, top N countries)
- Visualization settings (DPI, color palettes)
- Logging levels and output directories

## 🧪 Example Workflows

### Workflow 1: Global TB Trends
```python
from src.pipeline import TBAnalysisPipeline
pipeline = TBAnalysisPipeline()
pipeline.load_data()
pipeline.clean_data()
pipeline.analyze_owid()  # Focus on OWID trends
```

### Workflow 2: Program Performance
```python
pipeline = TBAnalysisPipeline()
pipeline.load_data()
pipeline.clean_data()
pipeline.analyze_who()   # Focus on WHO performance
```

### Workflow 3: Complete Analysis
```python
pipeline = TBAnalysisPipeline()
pipeline.run()  # Full pipeline with all analyses
```

## 📚 Documentation

- **config.py** - Comprehensive configuration settings with detailed comments
- **logger.py** - Logging configuration and utility functions
- **data_loader.py** - Data loading functions with error handling
- **data_cleaning.py** - Cleaning strategies for OWID and WHO data
- **analysis.py** - Analysis functions organized by data source
- **visualization.py** - Plot generation and figure management
- **pipeline.py** - Pipeline orchestration and execution
- **exploratory_analysis.ipynb** - Step-by-step interactive notebook

## 🐛 Troubleshooting

**Issue:** Missing data files
```
FileNotFoundError: OWID data file not found
```
**Solution:** Ensure CSV files are in `data/raw/` directory with correct names

**Issue:** Import errors
```
ModuleNotFoundError: No module named 'plotly'
```
**Solution:** Run `pip install -r requirements.txt` to install all dependencies

**Issue:** Output directory errors
```
FileNotFoundError: [Errno 2] No such file or directory: 'outputs/figures'
```
**Solution:** Directories are created automatically; check file permissions if needed

## 🤝 Contributing

This is an educational project demonstrating professional data science practices. Suggested improvements:
- Add additional statistical tests and analyses
- Expand visualization suite with more chart types
- Integrate real-time WHO/OWID API data
- Add predictive modeling
- Implement advanced geospatial analysis

## 📄 License

This project uses publicly available datasets from:
- [Our World in Data](https://ourworldindata.org/)
- [World Health Organization](https://www.who.int/)

## 👨‍💻 Author

Created as a demonstration of professional Python data science workflows for global health analysis.

## 📞 Questions & Support

For issues, questions, or suggestions, please refer to the code documentation and comments throughout the source files.

---

**Last Updated:** January 2026
