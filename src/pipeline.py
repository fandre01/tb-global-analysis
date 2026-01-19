"""
Main pipeline orchestration for TB Global Analysis project.
Coordinates data loading, cleaning, analysis, and visualization workflows.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logger
from config import (
    OWID_DATA_PATH, WHO_DATA_PATH,
    OWID_CLEANED_PATH, WHO_CLEANED_PATH,
    MERGED_DATA_PATH, MAX_YEAR
)
from data_loader import load_owid_data, load_who_data, validate_dataframe
from data_cleaning import clean_owid_data, clean_who_data
from analysis import (
    owid_global_tb_trends, owid_top_affected_countries, owid_country_incidence_trend,
    who_treatment_success_trends, who_top_performers, who_program_coverage_analysis,
    compare_incidence_vs_treatment_success
)
from visualization import (
    plot_global_tb_trends, plot_top_countries_comparison, plot_country_incidence_trend,
    plot_treatment_success_trends, plot_treatment_performers, plot_incidence_vs_treatment_scatter,
    animated_tb_map
)

logger = setup_logger(__name__)


class TBAnalysisPipeline:
    """Main pipeline for TB Global Analysis project."""
    
    def __init__(self):
        """Initialize the pipeline."""
        self.owid_raw = None
        self.who_raw = None
        self.owid_clean = None
        self.who_clean = None
        self.merged = None
        logger.info("TB Analysis Pipeline initialized")
    
    def load_data(self) -> bool:
        """
        Load raw data from OWID and WHO sources.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STAGE 1: DATA LOADING")
        logger.info("=" * 60)
        
        try:
            self.owid_raw = load_owid_data(str(OWID_DATA_PATH))
            self.who_raw = load_who_data(str(WHO_DATA_PATH))
            
            # Validate loaded data
            validate_dataframe(self.owid_raw, "OWID")
            validate_dataframe(self.who_raw, "WHO")
            
            logger.info("Data loading successful")
            return True
            
        except Exception as e:
            logger.error(f"Data loading failed: {e}")
            return False
    
    def clean_data(self) -> bool:
        """
        Clean and standardize data using source-specific strategies.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STAGE 2: DATA CLEANING")
        logger.info("=" * 60)
        
        try:
            self.owid_clean = clean_owid_data(self.owid_raw)
            self.who_clean = clean_who_data(self.who_raw)
            
            # Save cleaned datasets
            self.owid_clean.to_csv(OWID_CLEANED_PATH, index=False)
            logger.info(f"Saved cleaned OWID data to {OWID_CLEANED_PATH}")
            
            self.who_clean.to_csv(WHO_CLEANED_PATH, index=False)
            logger.info(f"Saved cleaned WHO data to {WHO_CLEANED_PATH}")
            
            logger.info("Data cleaning successful")
            return True
            
        except Exception as e:
            logger.error(f"Data cleaning failed: {e}")
            return False
    
    def analyze_owid(self) -> bool:
        """
        Perform OWID-specific analysis (high-level trends, geographic patterns).
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STAGE 3A: OWID ANALYSIS")
        logger.info("=" * 60)
        
        try:
            # Global trends
            logger.info("Analyzing global TB trends...")
            if 'tuberculosis_deaths' in self.owid_clean.columns:
                trends = owid_global_tb_trends(self.owid_clean)
                if not trends.empty:
                    plot_global_tb_trends(trends, 'tuberculosis_deaths')
                    logger.info("Global trends analysis complete")
            
            # Top affected countries
            logger.info("Identifying top affected countries...")
            latest_year = int(self.owid_clean['year'].max())
            top_countries = owid_top_affected_countries(self.owid_clean, year=latest_year, n=10)
            if not top_countries.empty:
                metric_col = top_countries.columns[-1]
                plot_top_countries_comparison(top_countries, latest_year, metric_col)
                logger.info(f"Top countries analysis complete ({latest_year})")
            
            # Country trend example
            logger.info("Analyzing country-level incidence trends...")
            if not self.owid_clean.empty:
                sample_countries = self.owid_clean['country'].unique()[:3]
                for country in sample_countries:
                    country_data = owid_country_incidence_trend(self.owid_clean, country)
                    if not country_data.empty:
                        plot_country_incidence_trend(country_data, country)
                logger.info(f"Country trends analysis complete")
            
            logger.info("OWID analysis successful")
            return True
            
        except Exception as e:
            logger.error(f"OWID analysis failed: {e}")
            return False
    
    def analyze_who(self) -> bool:
        """
        Perform WHO-specific analysis (program performance, treatment outcomes).
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STAGE 3B: WHO ANALYSIS")
        logger.info("=" * 60)
        
        try:
            # Treatment success trends
            logger.info("Analyzing treatment success trends...")
            if 'tb_treatment_success_rate' in self.who_clean.columns:
                success_trends = who_treatment_success_trends(self.who_clean)
                if not success_trends.empty:
                    plot_treatment_success_trends(success_trends)
                    logger.info("✓ Treatment success trends analysis complete")
            
            # Top performers
            logger.info("Identifying top-performing countries...")
            latest_year = int(self.who_clean['year'].max())
            performers = who_top_performers(self.who_clean, year=latest_year, n=10)
            if not performers.empty:
                plot_treatment_performers(performers, latest_year)
                logger.info(f"✓ Top performers analysis complete ({latest_year})")
            
            # Program coverage
            logger.info("Analyzing program coverage...")
            coverage = who_program_coverage_analysis(self.who_clean)
            if not coverage.empty:
                logger.info(f"✓ Program coverage analysis complete")
                logger.debug(f"Coverage data: {coverage.head()}")
            
            logger.info("WHO analysis successful")
            return True
            
        except Exception as e:
            logger.error(f"WHO analysis failed: {e}")
            return False
    
    def analyze_combined(self) -> bool:
        """
        Perform combined analysis with purposeful merging of OWID and WHO data.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STAGE 4: COMBINED ANALYSIS")
        logger.info("=" * 60)
        
        try:
            logger.info("Comparing TB incidence vs treatment success...")
            
            self.merged = compare_incidence_vs_treatment_success(self.owid_clean, self.who_clean)
            
            if not self.merged.empty:
                # Save merged data
                self.merged.to_csv(MERGED_DATA_PATH, index=False)
                logger.info(f"Saved merged data to {MERGED_DATA_PATH}")
                
                # Visualization
                plot_incidence_vs_treatment_scatter(self.merged)
                logger.info("Combined analysis complete")
            else:
                logger.warning("No overlapping data for combined analysis")
            
            logger.info("Combined analysis complete")
            return True
            
        except Exception as e:
            logger.error(f"Combined analysis failed: {e}")
            return False
    
    def generate_summary(self) -> None:
        """Generate and display analysis summary."""
        logger.info("=" * 60)
        logger.info("ANALYSIS SUMMARY")
        logger.info("=" * 60)
        
        if self.owid_clean is not None:
            logger.info(f"OWID Data: {len(self.owid_clean)} rows, {len(self.owid_clean.columns)} columns")
            logger.info(f"  Years: {int(self.owid_clean['year'].min())} - {int(self.owid_clean['year'].max())}")
            logger.info(f"  Countries: {self.owid_clean['country'].nunique()}")
        
        if self.who_clean is not None:
            logger.info(f"WHO Data: {len(self.who_clean)} rows, {len(self.who_clean.columns)} columns")
            logger.info(f"  Years: {int(self.who_clean['year'].min())} - {int(self.who_clean['year'].max())}")
            logger.info(f"  Countries: {self.who_clean['country'].nunique()}")
        
        if self.merged is not None:
            logger.info(f"Merged Data: {len(self.merged)} country-year combinations")
    
    def run(self) -> bool:
        """
        Execute the complete analysis pipeline.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("")
        logger.info("=" * 60)
        logger.info("TB GLOBAL ANALYSIS PIPELINE")
        logger.info("=" * 60)
        
        success = all([
            self.load_data(),
            self.clean_data(),
            self.analyze_owid(),
            self.analyze_who(),
            self.analyze_combined(),
        ])
        
        self.generate_summary()
        
        if success:
            logger.info("")
            logger.info("=" * 60)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)
        else:
            logger.error("")
            logger.error("=" * 60)
            logger.error("PIPELINE ENCOUNTERED ERRORS")
            logger.error("=" * 60)
        
        return success


def main():
    """Entry point for the analysis pipeline."""
    pipeline = TBAnalysisPipeline()
    success = pipeline.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
