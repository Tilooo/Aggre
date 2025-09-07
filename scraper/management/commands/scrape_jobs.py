import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraper.models import Job


class Command(BaseCommand):
    help = "Scrapes job listings from python.org/jobs/"

    def handle(self, *args, **kwargs):
        URL = "https://www.python.org/jobs/"

        self.stdout.write("Starting to scrape the job site...")

        try:
            response = requests.get(URL)
            response.raise_for_status()  # This will raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching the URL: {e}"))
            return

        soup = BeautifulSoup(response.content, 'lxml')
        jobs_list = soup.find('ol', class_='list-recent-jobs')

        if not jobs_list:
            self.stderr.write(
                self.style.ERROR("Could not find the job listings container. The site's HTML may have changed."))
            return

        job_elements = jobs_list.find_all('li')
        jobs_found = 0

        for job_element in job_elements:
            try:
                title_element = job_element.find('h2').find('span', class_='listing-company-name').find('a')
                title = title_element.text.strip()

                company_span = job_element.find('span', class_='listing-company-name')
                full_text = company_span.text.strip()
                company = full_text.split('\n')[-1].strip()

                location_element = job_element.find('span', class_='listing-location')
                location = location_element.text.strip()

                date_element = job_element.find('time')
                posted_date = date_element.text.strip()

                # --- The Django Part ---
                job_exists = Job.objects.filter(title=title, company=company, location=location).exists() # for duplicates

                if not job_exists:
                    Job.objects.create(
                        title=title,
                        company=company,
                        location=location,
                        posted_date=posted_date
                    )
                    jobs_found += 1

            except AttributeError:
                continue

        self.stdout.write(self.style.SUCCESS(f"Scraping finished. Found and saved {jobs_found} new jobs."))