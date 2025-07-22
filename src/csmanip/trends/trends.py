from .plot_warming_stripes import plot_annual_data, plot_monthly_data, plot_quarterly_data
from .identify_trends import analyze_trend
from .make_data_base import clean_missing_data, make_database, normalize_data
from .processing import read_csv
from .climdex import Climdex

class Trends:
    def analyze_trend(self, csv_file, column_name):
        return analyze_trend(csv_file, column_name)
    
    def read_csv(cities:list, output_dir):
        read_csv(cities, output_dir)

    def make_database(self, data, file_name):
        make_database(data, file_name)

    def clean_missing_data(self, df):
        clean_missing_data(df)

    def normalize_data(self, df):
        normalize_data(df)

    def plot_annual_data(self, csv_path, index, file_name, title_img, caption_img):
        plot_annual_data(csv_path, index, file_name, title_img, caption_img)

    def plot_monthly_data(self, csv_path, index, file_name, title_img, caption_img):
        plot_monthly_data(csv_path, index, file_name, title_img, caption_img)

    def plot_quarterly_data(self, csv_path, index, file_name, title_img, caption_img):
        plot_quarterly_data(csv_path, index, file_name, title_img, caption_img)