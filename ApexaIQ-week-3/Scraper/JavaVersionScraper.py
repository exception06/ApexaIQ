from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os


class JavaVersionScraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.driver = None
        os.makedirs(self.output_folder, exist_ok=True)

    def setup_driver(self):
        """Initialize the Selenium WebDriver."""
        self.driver = webdriver.Chrome()

    def fetch_table(self):
        """Navigate to the URL and fetch the version history table."""
        self.driver.get(self.url)
        try:
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[@class='wikitable sticky-header']")
                )
            )
            return table
        except Exception as e:
            print("Failed to locate table:", e)
            return None

    def parse_table(self, table):
        """Parse the table HTML into a pandas DataFrame."""
        headers = [th.text.strip() for th in table.find_elements(By.XPATH, ".//th")]
        rows = table.find_elements(By.XPATH, ".//tr")
        data = []

        for row in rows[1:]:
            cells = [td.text.strip() for td in row.find_elements(By.XPATH, ".//td")]
            if cells:
                data.append(cells)

        df = pd.DataFrame(data, columns=headers)
        return df

    def save_to_csv(self, df):
        """Save the DataFrame to a CSV file."""
        output_path = os.path.join(self.output_folder, self.output_file)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Data saved to {output_path}")

    def run(self):
        """Run the full scraping process."""
        try:
            self.setup_driver()
            table = self.fetch_table()
            if table:
                df = self.parse_table(table)
                self.save_to_csv(df)
            else:
                print("Table not found. Exiting.")
        except Exception as e:
            print("An error occurred during scraping:", e)
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    URL = "https://en.wikipedia.org/wiki/Java_version_history"
    OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
    OUTPUT_FILE = "java_version_history.csv"

    scraper = JavaVersionScraper(URL, OUTPUT_FOLDER, OUTPUT_FILE)
    scraper.run()
