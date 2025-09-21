# PyScrape Aggregator: A Personal Job Listings Web Scraper

PyScrape Aggregator is a powerful, personal job listings aggregator built from the ground up with Python and Django. This web application automatically scrapes job postings from multiple sources, saves them to a database, and displays them in a clean, stylish, and searchable web interface.

This project was built as a step-by-step learning journey, demonstrating key skills in web scraping, web development, and debugging in a real-world context.


---

## ✨ Features

-   **Multi-Source Scraping:** Gathers job listings from various websites, including:
    -   [Python.org Jobs](https://www.python.org/jobs/) (a static site)
    -   [RemoteOk.io](https://remoteok.com/) (a modern, JavaScript-driven site)
-   **Robust Scraping Engine:** Utilizes both `requests`/`BeautifulSoup` for simple sites and `Selenium` for handling complex, JavaScript-rendered content.
-   **Django-Powered Web Interface:** A user-friendly front-end to view and interact with the aggregated data.
-   **Dynamic Search:** Instantly filter job listings by keywords in the title or company name.
-   **Pagination:** A clean pagination system to easily navigate through hundreds of job listings.
-   **Database Persistence:** Scraped jobs are saved in a SQLite database to prevent data loss and avoid duplicate entries.
-   **Stylish & Modern UI:** A responsive, "glassmorphism" themed interface with a bright, professional design.

---

## 🛠️ Tech Stack

This project leverages a powerful stack of modern Python tools:

-   **Backend:** Python, Django
-   **Web Scraping:**
    -   `requests`: For fetching static HTML content.
    -   `BeautifulSoup4`: For parsing HTML and extracting data.
    -   `Selenium`: For controlling a web browser to scrape JavaScript-heavy websites.
-   **Database:** SQLite (default with Django)
-   **Development Environment:** PyCharm on Windows 10
-   **Experimentation:** Jupyter Notebook (for initial scraper development and testing)

---

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running on your machine.

### Prerequisites

-   Python 3.8+ ([Download](https://www.python.org/downloads/))
-   Pip (usually comes with Python)
-   Google Chrome (for the Selenium scraper)


## 🌟 Key Learning Outcomes & Project Journey

This project was a comprehensive exercise in solving real-world development problems:

-   **Adapting to Different Websites:** Successfully scraped both a simple static site and a modern site requiring JavaScript rendering.
-   **Debugging Anti-Scraping Measures:** Diagnosed and overcame challenges like CAPTCHAs and dynamic content loading by using Selenium and analyzing rendered HTML.
-   **Full-Stack Integration:** Seamlessly connected a Python scraping backend with a Django web frontend.
-   **Database Modeling & ORM:** Used Django's ORM to model data, create database tables with migrations, and write complex queries (filtering, ordering) without writing raw SQL.
-   **Modern UI/UX:** Implemented key features like search and pagination to create a polished and user-friendly experience.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page for this project.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
