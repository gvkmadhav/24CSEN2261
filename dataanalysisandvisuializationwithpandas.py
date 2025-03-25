#Chatgpt
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAnalysisError(Exception):
    """Custom exception for data analysis errors."""
    pass

class DataAnalyzer:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = None

    def load_data(self):
        """Load data from a CSV file into a Pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.data_file)
            logging.info(f"Data loaded from {self.data_file}.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            raise DataAnalysisError(f"Error loading data from {self.data_file}: {e}")
    
    def analyze_data(self):
        """Perform basic data analysis (summary stats, missing values)."""
        try:
            logging.info("Analyzing data...")
            summary = self.data.describe()  # Summary statistics
            missing_data = self.data.isnull().sum()  # Count missing values
            logging.info(f"Summary Statistics:\n{summary}")
            logging.info(f"Missing Data:\n{missing_data}")
            return summary, missing_data
        except Exception as e:
            logging.error(f"Failed to analyze data: {e}")
            raise DataAnalysisError(f"Error during data analysis: {e}")
    
    def visualize_data(self):
        """Create visualizations (histograms and scatter plots)."""
        try:
            logging.info("Visualizing data...")
            
            # Histogram of numerical columns
            self.data.hist(figsize=(10, 8), bins=20)
            plt.suptitle('Histograms of Numerical Columns')
            plt.show()

            # Scatter plot for two variables (assuming 'X' and 'Y' columns exist)
            if 'X' in self.data.columns and 'Y' in self.data.columns:
                self.data.plot.scatter(x='X', y='Y', alpha=0.5)
                plt.title('Scatter Plot of X vs Y')
                plt.show()
            else:
                logging.warning("'X' and 'Y' columns not found for scatter plot.")

        except Exception as e:
            logging.error(f"Failed to visualize data: {e}")
            raise DataAnalysisError(f"Error during data visualization: {e}")

    def run(self):
        """Run the data analysis and visualization pipeline."""
        try:
            self.load_data()
            self.analyze_data()
            self.visualize_data()
        except DataAnalysisError as e:
            logging.error(f"Data analysis failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

# Example usage
def main():
    data_file = 'data.csv'  # Replace with the path to your CSV file

    analyzer = DataAnalyzer(data_file)
    analyzer.run()

if __name__ == "__main__":
    main()
