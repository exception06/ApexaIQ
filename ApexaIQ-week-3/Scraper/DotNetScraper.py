from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

class DotNetScraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.driver = webdriver.Chrome()
        
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def start_scraping(self):
        """Main function to start the scraping process."""
        self.driver.get(self.url)
        dataframes = []

        try:
            # Wait for all tables to load
            tables = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@class='table table-bordered table-sm']"))
            )

            headings = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//h3"))
            )

            for i, table in enumerate(tables):
                table_name = headings[i].text.strip() if i < len(headings) else f"Table {i+1}"
                print(f"Scraping: {table_name}")

                html_content = table.get_attribute("outerHTML")
                df = pd.read_html(html_content)[0]

                name_df = pd.DataFrame([[table_name]], columns=df.columns[:1])
                blank_row = pd.DataFrame([[" "]*len(df.columns)], columns=df.columns)

                dataframes.extend([name_df, df, blank_row])

            # Combine all dataframes
            final_df = pd.concat(dataframes, ignore_index=True)

            # Save the final dataframe to CSV
            self.save_to_csv(final_df)

            print(f"All tables scraped and saved as {os.path.join(self.output_folder, self.output_file)}")

        except Exception as e:
            print("Error:", e)

        finally:
            self.driver.quit()

    def save_to_csv(self, dataframe):
        """Save the collected data to a CSV file."""
        output_path = os.path.join(self.output_folder, self.output_file)
        dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")


# Usage
URL = "https://dotnet.microsoft.com/en-us/download/dotnet/8.0"
OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
OUTPUT_FILE = "dotnet_8_0.csv"

scraper = DotNetScraper(URL, OUTPUT_FOLDER, OUTPUT_FILE)
scraper.start_scraping()
