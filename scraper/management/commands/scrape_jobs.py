from django.core.management.base import BaseCommand
from scraper.scrapers import python_org_scraper
from scraper.scrapers import remoteok_scraper


class Command(BaseCommand):
    help = "Scrapes job listings from multiple sites."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the scraping process...")

        # scrapers call
        python_org_scraper.scrape()
        remoteok_scraper.scrape()

        self.stdout.write(self.style.SUCCESS("All scraping finished."))