import pandas as pd
import numpy as np
import pathlib
import re
from datetime import datetime


class vert_export_handler:
    def __init__(
            self,
            raw_data_path=pathlib.Path.home() / 'Downloads',
            file_pattern = 'TeamCustomPlayerBreakdown*.xlsx', 
            session_sheet = 'Core Player Breakdown',
            period_sheet = 'Core Event Label Breakdown',
            save_csv=False, 
            col_thresh=18,
            column_rename = {
            'EVENT LABEL': 'Period Name',
            # 'PLAYER NAME': 'Player Name',
            'EVENT ID': 'Period Number',
            'DATE': 'Date'
            },
            drop_columns = ['PLAYER ID']
    ):
        self.file_pattern = file_pattern
        self.session_sheet = session_sheet
        self.period_sheet = period_sheet
        self.save_csv = save_csv
        self.col_thresh = col_thresh
        self.column_rename = column_rename
        self.drop_columns = drop_columns
        self.raw_data_path = raw_data_path

    def load_vert_data(self):
        most_recent_file = self.find_recent_file()
        self.period_df = pd.read_excel(
            most_recent_file,
            sheet_name=self.period_sheet,
            skiprows=5
        )
        self.period_df.rename(columns=self.column_rename, inplace=True)
        self.period_df.drop(columns=self.drop_columns, inplace=True)
        self.period_df['Period Number'] = self.period_df['Period Number'].map({
            val: i + 1 for i, val in enumerate(np.sort(self.period_df['Period Number'].unique()))
        })
        self.session_df = pd.read_excel(
            most_recent_file,
            sheet_name=self.session_sheet,
            skiprows=5
        )
        self.session_df.rename(columns=self.column_rename, inplace=True)
        self.session_df.drop(columns=self.drop_columns, inplace=True)
        self.session_df['Period Name'] = 'Session'
        self.session_df['Period Number'] = 0

        # Combine and clean
        self.upload_df = pd.concat([self.session_df, self.period_df])
        self.upload_df.dropna(thresh=self.col_thresh, inplace=True)
        self.upload_df = self.upload_df.sort_values(by=['PLAYER NAME', 'Period Number']).reset_index(drop=True)
        if len(pd.to_datetime(self.upload_df['Date']).unique())> 1:
            self.upload_df['Date'] = pd.to_datetime(self.upload_df['Date']).apply(lambda x: x.strftime("%m/%d/%Y")).min()
        if self.save_csv:
            date_str = self.extract_date_from_filename(most_recent_file.name)
            if date_str:
                self.upload_file_path = most_recent_file.parent / f"{date_str}.csv"
                self.upload_df.to_csv(
                    most_recent_file.parent / str(date_str+'.csv'),
                    index=False
                )
            else:
                print(f"Could not extract date from filename: {most_recent_file.name}. CSV not saved.")


    def find_recent_file(self):
        matching_files = list(self.raw_data_path.glob(self.file_pattern))
        if not matching_files:
            raise FileNotFoundError("No matching VERT files found in {self.raw_data_path}.")
        return max(matching_files, key=lambda f: f.stat().st_mtime)
    
    def extract_date_from_filename(self, filename):
        # Example: TeamCustomPlayerBreakdown.Oregon_VB_25.Aug-8-2025.xlsx
        match = re.search(r'([A-Za-z]+)-(\d+)-(\d{4})', filename)
        if match:
            month_str, day, year = match.groups()
            # Convert month name to month number
            try:
                month_num = datetime.strptime(month_str, "%b").month
            except ValueError:
                month_num = datetime.strptime(month_str, "%B").month
            date_obj = datetime(int(year), int(month_num), int(day))
            return date_obj.strftime("%Y%m%d")
        else:
            return None