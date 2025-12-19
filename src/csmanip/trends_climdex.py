from .trends.plot_warming_stripes import plot_annual_data, plot_monthly_data, plot_quarterly_data
from .trends.identify_trends import analyze_trend, analyze_indicator_trend
from .trends.make_data_base import clean_missing_data, make_database, normalize_data
from .trends.processing import process_csv
from .trends.group_data import group_data
from .trends.climdex import Climdex

class Trends():
    def analyze_trend(self, csv_file, column_name):
        return analyze_trend(csv_file, column_name)
    
    def analyze_indicator_trend(self, file_path):
        return analyze_indicator_trend(file_path)
    
    def group_data(self, cities:list, input_dir: str, output_dir:str):
        group_data(cities, input_dir, output_dir)
    
    def process_csv(self, cities:list, input_dir, output_dir):
        process_csv(cities, input_dir, output_dir)

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

    def read_files_climdex(self, processed_dir: str, station_names: list):
        c = Climdex()
        return c.read_files_climdex(processed_dir, station_names)
    
    def calculate_indices(self, df, base_period: tuple):
        c = Climdex()
        return c.calculate_indices(df, base_period)
    
    def write_indices(self, indices_ds, name, output_dir):
        c = Climdex()
        c.write_indices(indices_ds, name, output_dir)

    def plot_and_save_indices(self, indices_ds, name, output_dir):
        c = Climdex()
        c.plot_and_save_indices(indices_ds, name, output_dir)