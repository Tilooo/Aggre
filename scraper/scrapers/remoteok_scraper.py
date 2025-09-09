# scraper/scrapers/remoteok_scraper.py

import time
from bs4 import BeautifulSoup
from scraper.models import Job

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape():
    """Scrapes Python jobs from RemoteOk.io using Selenium to handle JavaScript."""
    print("Scraping RemoteOk.io with Selenium...")

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)

    URL = "https://remoteok.com/remote-python-jobs"

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.job[data-id]")))
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        job_elements = soup.find_all('tr', class_='job', attrs={'data-id': True})
        new_jobs_found = 0

        for job_element in job_elements:
            try:
                # LINK SELECTOR
                relative_link = job_element.get('data-url')
                if not relative_link:
                    continue

                link = f"https://remoteok.com{relative_link}"

                if Job.objects.filter(link=link).exists():
                    continue

                title = job_element.find('h2', itemprop='title').text.strip()
                company = job_element.find('h3', itemprop='name').text.strip()

                location_tags = job_element.find_all('div', class_='location')
                location = " / ".join([loc.text.strip() for loc in location_tags])

                posted_date = job_element.find('time').text.strip() if job_element.find('time') else "Not specified"

                Job.objects.create(
                    title=title,
                    company=company,
                    location=location,
                    posted_date=posted_date,
                    link=link
                )
                new_jobs_found += 1

            except (AttributeError, TypeError):
                continue

        print(f"Found and saved {new_jobs_found} new jobs from RemoteOk.io.")

    finally:
        driver.quit()