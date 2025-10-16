from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

class WindowsServerReleaseScraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.today = pd.Timestamp.now().strftime("%d-%m-%Y")
        self.driver = self.setup_driver()
        self.all_data = []  # Store final CSV rows

        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def setup_driver(self):
        """Setup Chrome WebDriver with necessary options."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    def scrape_table(self, table):
        """Extract data from a table."""
        # Extract headers
        headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

        # If no <th> headers, use first row as headers
        if not headers:
            first_row = table.find_elements(By.TAG_NAME, "tr")[0]
            headers = [td.text.strip() for td in first_row.find_elements(By.TAG_NAME, "td")]

        num_headers = len(headers)
        if num_headers == 0:
            return []  # skip empty tables

        # Add header row to CSV
        data = [{headers[i]: headers[i] for i in range(num_headers)}]

        # Extract table rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        start_index = 1 if table.find_elements(By.TAG_NAME, "th") else 1
        for row in rows[start_index:]:
            cells = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            if cells:
                # Pad cells to match headers
                while len(cells) < num_headers:
                    cells.append("")
                row_data = {headers[i]: cells[i] for i in range(num_headers)}
                row_data["Scraped Date"] = self.today
                data.append(row_data)

        # Add a blank row to separate tables
        data.append({})
        return data

    def scrape_data(self):
        """Main scraping function that extracts all tables."""
        try:
            self.driver.get(self.url)

            # Wait for all tables on the page to load
            tables = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table"))
            )

            # Scrape each table
            for idx, table in enumerate(tables):
                print(f"Scraping table {idx + 1}...")
                table_data = self.scrape_table(table)
                self.all_data.extend(table_data)

        except Exception as e:
            print(f"Error scraping tables: {e}")

    def save_to_csv(self):
        """Save the scraped data to a CSV file."""
        if not self.all_data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.all_data)
        output_path = os.path.join(self.output_folder, self.output_file)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"All tables scraped successfully and saved to {output_path}")

    def run(self):
        """Run the scraper."""
        self.scrape_data()
        self.save_to_csv()

    def quit_driver(self):
        """Quit the web driver."""
        self.driver.quit()


# Usage
URL = "https://learn.microsoft.com/en-us/windows/release-health/windows-server-release-info"
OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
OUTPUT_FILE = "windows_server_release_info.csv"

scraper = WindowsServerReleaseScraper(URL, OUTPUT_FOLDER, OUTPUT_FILE)
scraper.run()
scraper.quit_driver()
