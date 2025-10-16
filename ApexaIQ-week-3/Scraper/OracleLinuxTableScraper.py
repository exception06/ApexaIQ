from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os


class OracleLinuxTableScraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.driver = None
        os.makedirs(self.output_folder, exist_ok=True)

    def setup_driver(self):
        """Initialize the Selenium WebDriver."""
        self.driver = webdriver.Chrome()

    def extract_table_data(self, table):
        """Extract headers and rows from a single table and return a DataFrame."""
        headers = [th.text.strip() for th in table.find_elements(By.XPATH, ".//th")]
        num_headers = len(headers)
        rows = table.find_elements(By.XPATH, ".//tr")
        data = []

        for row in rows[1:]:
            cells = [td.text.strip() for td in row.find_elements(By.XPATH, ".//td")]
            if cells:
                while len(cells) < num_headers:
                    cells.append("")  # pad missing cells
                data.append(cells)

        return pd.DataFrame(data, columns=headers)

    def scrape_tables(self):
        """Scrape all tables on the page with class containing 'wikitable'."""
        self.driver.get(self.url)
        tables = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table[contains(@class, 'wikitable')]")
            )
        )
        all_data = []

        for idx, table in enumerate(tables):
            df = self.extract_table_data(table)

            # Add a title row
            df.loc[-1] = [f"Table {idx + 1}"] + [""] * (df.shape[1] - 1)
            df.index = df.index + 1
            df = df.sort_index()

            all_data.append(df)
            # Add a blank row between tables
            all_data.append(pd.DataFrame([[""] * df.shape[1]], columns=df.columns))

        final_df = pd.concat(all_data, ignore_index=True, sort=False)
        return final_df

    def save_to_csv(self, df):
        """Save the final DataFrame to CSV."""
        output_path = os.path.join(self.output_folder, self.output_file)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"All tables scraped successfully and saved as {self.output_file}!")

    def run(self):
        """Run the complete scraping process."""
        try:
            self.setup_driver()
            final_df = self.scrape_tables()
            self.save_to_csv(final_df)
        except Exception as e:
            print("Error:", e)
        finally:
            if self.driver:
                self.driver.quit()


# --- Entry Point ---
if __name__ == "__main__":
    URL = "https://en.wikipedia.org/wiki/Oracle_Linux"
    OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
    OUTPUT_FILE = "Oracle_Linux.csv"

    scraper = OracleLinuxTableScraper(URL, OUTPUT_FOLDER, OUTPUT_FILE)
    scraper.run()
