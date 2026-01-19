"""
Configuration module for TB Global Analysis project.
Centralized management of paths, parameters, and project settings.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Output directories
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MAPS_DIR = OUTPUTS_DIR / "maps"

# Source data files
OWID_DATA_PATH = RAW_DATA_DIR / "tb_owid.csv"
WHO_DATA_PATH = RAW_DATA_DIR / "tb_who.csv"

# Processed output files
OWID_CLEANED_PATH = PROCESSED_DATA_DIR / "tb_owid_cleaned.csv"
WHO_CLEANED_PATH = PROCESSED_DATA_DIR / "tb_who_cleaned.csv"
MERGED_DATA_PATH = PROCESSED_DATA_DIR / "tb_merged.csv"

# Analysis parameters
MIN_YEAR = 1990  # Start year for analysis
MAX_YEAR = 2023  # End year for analysis
TOP_N_COUNTRIES = 10  # Number of top countries to display
ANIMATION_SPEED = 500  # Animation speed in milliseconds

# Data quality thresholds
MIN_DATA_COVERAGE = 0.2  # Minimum data coverage for country inclusion
OUTLIER_ZSCORE = 3  # Z-score threshold for outlier detection

# Visualization settings
FIGURE_DPI = 300
FIGURE_FORMAT = "png"
PLOTLY_RENDERER = "browser"  # Options: 'browser', 'notebook', 'json'

# Color palettes
COLOR_PALETTE_TB = "Reds"  # Plotly color scale for TB incidence
COLOR_PALETTE_TREATMENT = "Blues"  # Color scale for treatment success rates

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "logs" / "tb_analysis.log"

# Ensure all directories exist
for directory in [PROCESSED_DATA_DIR, FIGURES_DIR, MAPS_DIR, LOG_FILE.parent]:
    directory.mkdir(parents=True, exist_ok=True)
