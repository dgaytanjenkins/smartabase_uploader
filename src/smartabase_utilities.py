import time
import pandas as pd
import numpy as np
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class smartabase_import_data:

    def __init__(self, 
                 upload_file_path, 
                 practice_date, 
                 start_time,
                 event_form = "Catapult CORE", 
                 username="", 
                 password="", 
                 player_column='Player Name',
                 driver_path=pathlib.Path.home() / 'Documents' / 'automate_boring_stuff' / 'catapult_uploader' / 'chromedriver-win64' / 'chromedriver.exe',
                 raw_data_path=pathlib.Path.home() / 'Downloads',
                 ):
        self.upload_file_path = upload_file_path
        self.practice_date = practice_date
        self.start_time = start_time
        self.event_form = event_form
        self.username = username
        self.password = password
        self.player_column = player_column
        self.driver_path = pathlib.Path(driver_path) if isinstance(driver_path, str) else driver_path
        self.download_path = raw_data_path
        self.driver = None

    def process_and_upload(self):
        self.setup_driver()
        self.login()
        self.change_group()
        self.navigate_to_import()
        self.select_event()
        self.upload_file()
        self.enter_date_time()
        self.finalize_import()
        

    def setup_driver(self):
        self.driver = webdriver.Chrome()#executable_path=str(self.driver_path))
        self.driver.get("https://oregon.smartabase.com/ducks/#Login")

    def login(self):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='usernameOrEmail']"))
        )
        username_field.send_keys(self.username)
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='password']"))
        )
        password_field.send_keys(self.password)
        login_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign in']"))
        )
        login_button.click()

    def change_group(self,group='volleyball-all',subgroup='lacrosse-current'):
        change_group_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'change-group')]"))
        )
        if change_group_element.get_attribute('id') != subgroup:
            change_group_element.click()
            all_users_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='all-users']"))
            )
            all_users_button.click()
            all_athletes_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='all-athletes']"))
            )
            all_athletes_button.click()
            lax_all_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='%s']" % group))
            )
            lax_all_button.click()
            lax_current_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='%s']" % subgroup))
            )
            lax_current_button.click()
            time.sleep(2)
            load_button = self.driver.find_element(By.XPATH, "//button[@type='button' and @id='load']")
            load_button.click()

    def navigate_to_import(self):
        dropdown_trigger = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'dropdown')]//span[text()='Data Entry']"))
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(dropdown_trigger).perform()
        import_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='import-data']"))
        )
        import_item.click()

    def select_event(self):
        select_event = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='dropdown-formselector-4']"))
        )
        event = Select(select_event)
        event.select_by_visible_text(self.event_form)

    def upload_file(self):
        upload_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='file' and @class='gwt-TextBox']"))
        )
        upload_input.send_keys(str(self.upload_file_path))
        upload_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @id='upload']"))
        )
        upload_button.click()
    
    def confirm_athlete_column(self):
        time.sleep(7)
        col_select = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@class='gwt-ListBox']"))
        )
        col_select = Select(col_select)
        col_select.select_by_visible_text(self.player_column)
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @id='next']"))
        )
        next_button.click()

    def enter_date_time(self):
        date_entry = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @class='gwt-DateBox']"))
        )
        date_entry.clear()
        date_entry.send_keys(self.practice_date)
        date_entry.click()

        select_box_wrapper = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.select-box-wrapper.time-picker"))
        )
        select_element = select_box_wrapper.find_element(By.CSS_SELECTOR, "select.gwt-ListBox")
        select_time = Select(select_element)
        select_time.select_by_visible_text(self.start_time)

        # check if Date column exists, if so swithc to MM/dd/yy
        date_col = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@class='gwt-ListBox' and @id='dropdown-column-37']"))
        )
        date_col_select = Select(date_col)
        date_col_select.select_by_value('')

        # Check if the label for treating records is present and click it
        label = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[text()='Treat all records for the same user, on the same day as a single record?']"))
        )
        checkbox_id = label.get_attribute('for')
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        checkbox.click()

        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @id='next']"))
        )
        next_button.click()

    def finalize_import(self):
        import_final = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @id='import']"))
        )
        import_final.click()

        # Optionally, close the driver
        # self.driver.quit()
