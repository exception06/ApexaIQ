from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os

class WikiScraper:
    def __init__(self, url, output_folder, output_file):
        self.url = url
        self.output_folder = output_folder
        self.output_file = output_file
        self.driver = self.setup_driver()
        self.title = ""
        self.intro = ""
        self.infobox_data = {}
        self.all_headers = []
        self.all_rows = []

        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    def fetch_page(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output")))

    def extract_title(self):
        self.title = self.driver.title

    def extract_intro(self):
        try:
            intro_elem = self.driver.find_element(By.CSS_SELECTOR, "div.mw-parser-output > p")
            self.intro = intro_elem.text.strip()
        except Exception:
            self.intro = ""

    def extract_infobox(self):
        try:
            infobox = self.driver.find_element(By.CSS_SELECTOR, "table.infobox")
            rows = infobox.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                ths = row.find_elements(By.TAG_NAME, "th")
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(ths) == 1 and len(tds) == 1:
                    key = ths[0].text.strip()
                    val = tds[0].text.strip()
                    self.infobox_data[key] = val
        except:
            pass

    def split_multi(self, cell_text):
        parts = re.split(r"\s*/\s*|\s*,\s*", cell_text.strip())
        return [p for p in parts if p]

    def expand_rows_for_multivals(self, headers, rows):
        expanded = []
        for row in rows:
            multi_header = None
            multi_values = None
            for h in headers:
                vals = self.split_multi(row.get(h, ""))
                if len(vals) > 1:
                    multi_header = h
                    multi_values = vals
                    break
            if multi_header is None:
                expanded.append(row)
            else:
                for v in multi_values:
                    new_row = dict(row)
                    new_row[multi_header] = v
                    expanded.append(new_row)
        need_more = any(len(self.split_multi(r.get(h, ""))) > 1 for r in expanded for h in headers)
        if need_more:
            return self.expand_rows_for_multivals(headers, expanded)
        return expanded

    def scrape_tables(self):
        tables = self.driver.find_elements(By.CSS_SELECTOR, "table.wikitable")
        for tbl in tables:
            ths = tbl.find_elements(By.TAG_NAME, "th")
            headers = [th.text.strip() for th in ths]
            if not headers:
                continue
            for h in headers:
                if h not in self.all_headers:
                    self.all_headers.append(h)

            trs = tbl.find_elements(By.TAG_NAME, "tr")
            rows = []
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, "td")
                if not tds:
                    continue
                vals = [td.text.strip() for td in tds]
                if len(vals) != len(headers):
                    continue
                row_dict = dict(zip(headers, vals))
                rows.append(row_dict)

            rows_expanded = self.expand_rows_for_multivals(headers, rows)
            for r in rows_expanded:
                for h in self.all_headers:
                    if h not in r:
                        r[h] = ""
                self.all_rows.append(r)

    def merge_page_info(self):
        if not self.all_rows:
            row = {"Title": self.title, "Introduction": self.intro}
            for k, v in self.infobox_data.items():
                row[k] = v
            self.all_rows = [row]
            self.all_headers = list(row.keys())
        else:
            for r in self.all_rows:
                r["Page_Title"] = self.title
                r["Introduction"] = self.intro
                for k, v in self.infobox_data.items():
                    r[k] = v
            for extra in ["Page_Title", "Introduction"] + list(self.infobox_data.keys()):
                if extra not in self.all_headers:
                    self.all_headers.append(extra)

    def save_to_csv(self):
        df = pd.DataFrame(self.all_rows, columns=self.all_headers)
        fname = self.clean_filename("SUSE_Linux_Enterprise") + ".csv"
        output_path = os.path.join(self.output_folder, fname)
        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path} — rows: {len(df)}")

    def clean_filename(self, s):
        return re.sub(r"[^0-9a-zA-Z_]+", "_", s)

    def scrape(self):
        try:
            self.fetch_page()
            self.extract_title()
            self.extract_intro()
            self.extract_infobox()
            self.scrape_tables()
            self.merge_page_info()
            self.save_to_csv()
        finally:
            self.driver.quit()


# Main execution
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/SUSE_Linux_Enterprise"
    OUTPUT_FOLDER = "ApexaIQ-week-3/Output"
    OUTPUT_FILE = "SUSE_Linux_Enterprise.csv"

    scraper = WikiScraper(url, OUTPUT_FOLDER, OUTPUT_FILE)
    scraper.scrape()
