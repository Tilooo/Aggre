# scraper/scrapers/stackoverflow_scraper.py

import time
from bs4 import BeautifulSoup
from scraper.models import Job

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import this exception


def scrape():
    print("Scraping new Stack Overflow (powered by Indeed) with Selenium...")

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)

    URL = "https://stackoverflowjobs.com/?q=Python"

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        # cookie banner
        try:
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
            print("Cookie banner found and 'Accept all' button clicked.")
            time.sleep(1)
        except TimeoutException:
            print("Cookie banner not found, continuing...")

        wait.until(EC.presence_of_element_located((By.ID, "job-list")))
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        job_list = soup.find('ul', id='job-list')
        if not job_list:
            print("Could not find the job list even after handling the cookie banner.")
            driver.quit()
            return

        job_elements = job_list.find_all('li')
        new_jobs_found = 0

        for job_element in job_elements:
            try:
                title_element = job_element.find('h2')
                title = title_element.text.strip() if title_element else "No Title"

                job_div = job_element.find('div', attrs={'data-jobkey': True})
                job_key = job_div['data-jobkey'] if job_div else None
                if not job_key: continue

                link = f"https://stackoverflowjobs.com/job/{job_key}"

                if Job.objects.filter(link=link).exists(): continue

                company_element = job_element.find('p', class_='css-1pnk0le')
                company = company_element.text.strip() if company_element else "No Company"

                location_element = job_element.find('p', class_='css-u7ev33')
                location = location_element.text.strip() if location_element else "No Location"

                date_element = job_element.find('p', class_='css-13x1vyp')
                posted_date = date_element.text.strip() if date_element else "Not specified"

                Job.objects.create(
                    title=title,
                    company=company,
                    location=location,
                    posted_date=posted_date,
                    link=link
                )
                new_jobs_found += 1

            except Exception:
                continue

        print(f"Found and saved {new_jobs_found} new jobs from Stack Overflow (Indeed).")

    finally:
        driver.quit()