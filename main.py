from playwright.sync_api import sync_playwright
from time import sleep
from rich.console import Console
from rich.table import Table
from random import randint
'''
pip install playwright  
playwright install 
pip install rich
'''
jobTitle = input("Job Title : ")
jobLocation = input("Job Location : ")
counter = 0
console = Console()
with sync_playwright() as p:
    browser = p.chromium.launch()
    while True:
        page = browser.new_page()
        url = f"https://www.linkedin.com/jobs/search/?&keywords={jobTitle}&location={jobLocation}&refresh=true&start={counter}"
        page.goto(url)
        job_card = page.locator("li").all()
        #create rich table
        table = Table(title=f"{jobTitle} jobs in {jobLocation}")
        table.add_column("Title")
        table.add_column("Location")
        table.add_column("Company")
        table.add_column("Url", overflow="fold")
        #loop over each possible card
        for card in job_card:
            title = card.locator(".base-search-card__title")
            location = card.locator(".job-search-card__location")
            company = card.locator(".base-search-card__subtitle a")
            link = card.locator(".base-card__full-link")
            #if data is there then use it 
            if title.count() > 0 and location.count() > 0 and company.count() > 0 and link.count() > 0 :
                title = title.first.inner_html().strip()  
                location = location.first.inner_html().strip()  
                company = company.first.inner_html().strip()  
                link = link.get_attribute("href")
                #add row to table
                table.add_row(title, location, company, link)
        #print rich table to std out
        console.print(table)
        continueScraping = input("Continue to next page (y/n)")
        if continueScraping.strip() == "y":
            counter += 25
            #close page since we are done with it 
            page.close()
            #sleep before moving to next page to seem less sus
            sleep(randint(1,10))
        else:
            break
    browser.close()
