# scrape.py
from playwright.sync_api import sync_playwright
from time import sleep
from random import randint
import os

jobTitle = os.getenv("JOB_TITLE", "Software Engineer")
jobLocation = os.getenv("JOB_LOCATION", "Toronto")
max_pages = 1
counter = 0

readme_content = f"# {jobTitle} jobs in {jobLocation}\n\n"

with sync_playwright() as p:
    browser = p.chromium.launch()
    for _ in range(max_pages):
        page = browser.new_page()
        url = f"https://www.linkedin.com/jobs/search/?keywords={jobTitle}&location={jobLocation}&refresh=true&start={counter}"
        page.goto(url)
        job_card = page.locator("li").all()

        for card in job_card:
            title = card.locator(".base-search-card__title")
            location = card.locator(".job-search-card__location")
            company = card.locator(".base-search-card__subtitle a")
            link = card.locator(".base-card__full-link")

            if title.count() > 0 and location.count() > 0 and company.count() > 0 and link.count() > 0:
                readme_content += f"- **{title.first.inner_html().strip()}** at {company.first.inner_html().strip()} — {location.first.inner_html().strip()}  \n  [Apply Here]({link.get_attribute('href')})\n"

        page.close()
        counter += 25
        sleep(randint(1, 3))
    browser.close()

# Save to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)