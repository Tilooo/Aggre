# scraper/scrapers/python_org_scraper.py

import requests
from bs4 import BeautifulSoup
from scraper.models import Job


def scrape():
    """Scrapes jobs from python.org and saves them to the database."""
    print("Scraping Python.org...")

    URL = "https://www.python.org/jobs/"
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching python.org: {e}")
        return

    soup = BeautifulSoup(response.content, 'lxml')
    jobs_list = soup.find('ol', class_='list-recent-jobs')

    if not jobs_list:
        print("Could not find the job listings container on Python.org.")
        return

    job_elements = jobs_list.find_all('li')
    new_jobs_found = 0

    for job_element in job_elements:
        try:
            title_element = job_element.find('h2').find('span', class_='listing-company-name').find('a')
            title = title_element.text.strip()
            relative_link = title_element['href']
            link = f"https://www.python.org{relative_link}"

            job_exists = Job.objects.filter(link=link).exists()
            if job_exists:
                continue

            company_span = job_element.find('span', class_='listing-company-name')
            full_text = company_span.text.strip()
            company = full_text.split('\n')[-1].strip()

            location_element = job_element.find('span', class_='listing-location')
            location = location_element.text.strip()

            date_element = job_element.find('time')
            posted_date = date_element.text.strip()

            Job.objects.create(
                title=title,
                company=company,
                location=location,
                posted_date=posted_date,
                link=link
            )
            new_jobs_found += 1

        except AttributeError:
            continue

    print(f"Found and saved {new_jobs_found} new jobs from Python.org.")