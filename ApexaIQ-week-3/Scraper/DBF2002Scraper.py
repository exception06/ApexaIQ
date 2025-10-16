from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import re
import os


class DBF2002Scraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.driver = webdriver.Chrome()

        # Make sure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def start_scraping(self):
        """Main function to start the scraping process."""
        self.driver.get(self.url)
        data = []

        try:
            h3_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//h3"))
            )

            for h3 in h3_elements:
                text = h3.text.strip()

                version, formatted_date = self.extract_version_and_date(text)

                data.append({
                    "Version": version,
                    "Date": formatted_date,
                    "URL": self.url
                })

            self.save_to_csv(data)
            print(f"Table scraped successfully and saved as {self.output_file}!")

        except Exception as e:
            print("Error:", e)

        finally:
            self.driver.quit()

    def extract_version_and_date(self, text):
        """Extract version and date from the text."""
        version_match = re.search(r"(v[^\s]+)", text)
        version = version_match.group(1) if version_match else None

        date_match = re.search(r"\(([^)]+)\)", text)
        date_str = date_match.group(1) if date_match else None

        formatted_date = None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
                formatted_date = date_obj.strftime("%m/%d/%y")
            except ValueError:
                formatted_date = "Invalid Date"

        return version, formatted_date

    def save_to_csv(self, data):
        """Save the scraped data to a CSV file."""
        df = pd.DataFrame(data)
        output_path = os.path.join(self.output_folder, self.output_file)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")


# Usage
URL = "https://www.dbf2002.com/news.html"
OUTPUT_FOLDER = "ApexaIQ-week-3"
OUTPUT_FILE = "dbf2002.csv"

scraper = DBF2002Scraper(URL, OUTPUT_FOLDER, OUTPUT_FILE)
scraper.start_scraping()
