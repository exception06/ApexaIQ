from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os


class WebScraper:
    def __init__(self, url, output_folder, tables_info):
        self.url = url
        self.output_folder = output_folder
        self.tables_info = tables_info
        self.driver = webdriver.Chrome()

        # Make sure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        self.today = pd.Timestamp.now().strftime("%d-%m-%Y")

    def start_scraping(self):
        """Main function to start the scraping process."""
        self.driver.get(self.url)
        all_rows = []

        for table_info in self.tables_info:
            all_rows.extend(self.scrape_table(table_info))

        self.driver.quit()

        # Save data to CSV
        self.save_to_csv(all_rows)
        print(f"Both tables saved successfully to {os.path.join(self.output_folder, 'core_8_0_0_all_tables.csv')}")

    def scrape_table(self, table_info):
        """Scrape a single table from the page."""
        all_rows = []
        try:
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, table_info["xpath"]))
            )

            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            all_rows.append({headers[0]: table_info["name"]})

            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows[1:]:  # Skip header row
                cells = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
                if cells:
                    row_data = {headers[j]: cells[j] if j < len(cells) else "" for j in range(len(headers))}
                    row_data["Scraped Date"] = self.today
                    all_rows.append(row_data)

            all_rows.append({})  # Add an empty row after each table

        except Exception as e:
            print(f"Error scraping {table_info['name']}: {e}")

        return all_rows

    def save_to_csv(self, all_rows):
        """Save the scraped data to a CSV file."""
        df = pd.DataFrame(all_rows)
        output_file = os.path.join(self.output_folder, "core_8_0_0_all_tables.csv")
        df.to_csv(output_file, index=False, encoding="utf-8-sig")


# Usage
URL = "https://versionsof.net/core/8.0/8.0.0/"
OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
TABLES_INFO = [
    {"xpath": "(//table)[1]", "name": "Download Table"},
    {"xpath": "(//table)[2]", "name": "Updated Packages"}
]

scraper = WebScraper(URL, OUTPUT_FOLDER, TABLES_INFO)
scraper.start_scraping()
