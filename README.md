# Smartabase Uploader Utilities

This project provides utilities for processing and uploading Catapult (OpenField) and Vert data to Smartabase using Python classes and Selenium automation.

## Project Structure

```
smartabase_uploader
├── src
│   ├── catapult_utilites.py      # Catapult/OpenField data processing
│   ├── vert_utilities.py         # Vert data processing
│   ├── smartabase_utilities.py   # Smartabase upload automation
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Installation

Install dependencies with:

```
pip install -r requirements.txt
```

## Usage

### 1. Process Vert Data and Upload to Smartabase

```python
import vert_utilities as vu
import smartabase_utilities as smu

# Process Vert data
vert_handler = vu.vert_export_handler(save_csv=True)
vert_handler.load_vert_data()

# Prepare Smartabase uploader
sm_importer = smu.smartabase_import_data(
    vert_handler.upload_file_path,
    "Mon, 08-11-2025",      # Practice date
    '3:00 PM',              # Start time
    event_form="Vert",      # Event form name in Smartabase
    player_column='PLAYER NAME'
)

# Step through the upload process
sm_importer.setup_driver()
sm_importer.login()
sm_importer.change_group(group='volleyball-all', subgroup="volleyball-indoor-current")
sm_importer.navigate_to_import()
sm_importer.select_event()
sm_importer.upload_file()
sm_importer.confirm_athlete_column()
sm_importer.enter_date_time()
sm_importer.finalize_import()
```

### 2. Process Catapult Data

```python
import catapult_utilites as cu

cat_handler = cu.catapult_export_handler(output_name="output.csv")
cat_handler.load_catapult_data()
missing = cat_handler.missing_athletes("roster.csv")
```

### Notes

- The utilities expect your raw data files to be in your `Downloads` folder by default.
- For Vert data, the processed CSV will be saved automatically if `save_csv=True`.
- You may need to adjust `event_form` and `player_column` to match your Smartabase configuration.
- **[Download ChromeDriver here](https://sites.google.com/chromium.org/driver/)** and ensure it is installed and available in your PATH.

## Classes and Methods

### `catapult_export_handler`
- `load_catapult_data()`: Loads and sorts Catapult data.
- `find_recent_file()`: Finds the latest matching Catapult file.
- `missing_athletes(roster_path)`: Compares loaded data to a roster CSV.

### `vert_export_handler`
- `load_vert_data()`: Loads and processes Vert data, saves CSV if specified.
- `find_recent_file()`: Finds the latest matching Vert file.

### `smartabase_import_data`
- `setup_driver()`: Initializes Selenium WebDriver.
- `login()`: Logs into Smartabase.
- `change_group(group, subgroup)`: Changes user/group context.
- `navigate_to_import()`: Navigates to import section.
- `select_event()`: Selects the event form.
- `upload_file()`: Uploads the processed CSV.
- `confirm_athlete_column()`: Confirms the athlete column.
- `enter_date_time()`: Enters date and time for the session.
- `finalize_import()`: Finalizes the import process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements