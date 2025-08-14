import pandas as pd
import numpy as np
import pathlib

class catapult_export_handler:
    def __init__(self, output_name, raw_data_path=pathlib.Path.home() / 'Downloads',file_pattern='ctr-report-*.csv'):
        self.output_name = output_name
        self.raw_data_path = raw_data_path  
        self.file_pattern = file_pattern

    def load_catapult_data(self):
        most_recent_file = self.find_recent_file()
        df = pd.read_csv(most_recent_file, skiprows=9, header=0)
        self.upload_df = df.sort_values(by=['Player Name', 'Period Number'])

    def find_recent_file(self):
        matching_files = list(self.raw_data_path.glob(self.file_pattern))
        if not matching_files:
            raise FileNotFoundError("No matching Openfield files found in {self.raw_data_path}.")
        return max(matching_files, key=lambda f: f.stat().st_mtime)
    
    def missing_athletes(self, roster_path):
        if not hasattr(self, 'upload_df'):
            raise ValueError("Data not loaded. Please run load_catapult_core_data() first.")
        
        roster_df = pd.read_csv(roster_path)
        if 'Player Name' not in roster_df.columns:
            roster_df['Player Name'] = roster_df['firstname']+' '+roster_df['lastname']
        return set(list(roster_df['Player Name'].values)) - set(list(self.upload_df['Player Name'].unique()))