from playwright.sync_api import sync_playwright
from time import sleep

'''
pip install playwright  
playwright install 
'''

jobTitle = input("Job Title : ")
jobLocation = input("Job Location : ")
counter = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    while True:
        page = browser.new_page()
        url = f"https://www.linkedin.com/jobs/search/?&keywords={jobTitle}&location={jobLocation}&refresh=true&start={counter}"
        page.goto(url)

        #wait for the job list to appear
        page.wait_for_selector(".jobs-search__results-list")

        job_card = page.locator("li").all()
        
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

                print(f"{title} {location} {company} {link}")
            
        continueScraping = input("Continue to next page (y/n)")
        if continueScraping.strip() == "y":
            counter += 25
            #close page since we are done with it 
            page.close()
            #sleep before moving to next page to seem less sus
            sleep(3)
        else:
            break

    browser.close()
