# web scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# html parsing
from bs4 import BeautifulSoup
# dataframes
import pandas as pd
# async
import asyncio
# terminal formatting
from rich.progress import track
from rich.console import Console
from rich.table import Table

# intantiate global variables
df = pd.DataFrame(columns=['Title', 'Location', 'Company', 'Link'])
console = Console()
table = Table(show_header=True, header_style="bold")

# get user input
console.print("Enter Job Title :", style="bold green", end=" ")
inputJobTitle = input()
console.print("Enter Job Location :", style="bold green", end=" ")
inputJobLocation = input()


async def scrapeBebee():
    global df
    global inputJobTitle
    global inputJobLocation

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(
        f"https://ca.bebee.com/jobs?term={inputJobTitle}&location={inputJobLocation}")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ulElement = soup.find('ul', class_='jobs_list_scroll')
    liElements = ulElement.find_all('li')

    for item in track(liElements, description="Bebee"):
        jobTitle = item.find('h2', class_='mb-0').text.strip()

        # TODO
        jobCompany = ""
        jobLocation = ""
        jobLink = ""

        df = pd.concat([df, pd.DataFrame({'Title': [jobTitle], 'Location': [
                       jobLocation], 'Company': [jobCompany], 'Link': [
            jobLink]})], ignore_index=True)

    driver.quit()


async def scrapeEluta():
    global df
    global inputJobTitle
    global inputJobLocation

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(
        f"https://www.eluta.ca/search?q={inputJobTitle}&l={inputJobLocation}&qc=")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    jobList = soup.findAll('div', class_='organic-job')

    for job in track(jobList, description="Eluta"):
        jobTitle = job.find('h2', class_='title').text.strip()
        jobLocation = job.find(
            'span', class_='location').text.strip()
        jobCompany = job.find(
            'a', class_='employer').text.strip()
        jobLink = job.find('a', class_='lk-job-title')['href']

        df = pd.concat([df, pd.DataFrame({'Title': [jobTitle], 'Location': [
                       jobLocation], 'Company': [jobCompany], 'Link': [
            jobLink]})], ignore_index=True)

    driver.quit()


async def scrapeLinkedin():
    global df
    global inputJobTitle
    global inputJobLocation

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(
        f"https://www.linkedin.com/jobs/search/?&keywords={inputJobTitle}&location={inputJobLocation}&refresh=true")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ulElement = soup.find('ul', class_='jobs-search__results-list')
    liElements = ulElement.find_all('li')

    for item in track(liElements, description="Linkedin"):
        jobTitle = item.find(
            'h3', class_='base-search-card__title').text.strip()
        jobLocation = item.find(
            'span', class_='job-search-card__location').text.strip()
        jobCompany = item.find(
            "h4", class_="base-search-card__subtitle").text.strip()
        jobLink = ""

        df = pd.concat([df, pd.DataFrame({'Title': [jobTitle], 'Location': [
                       jobLocation], 'Company': [jobCompany], 'Link': [
            jobLink]})], ignore_index=True)

    driver.quit()


async def main():
    # call all scraping functions
    tasks = [
        asyncio.create_task(scrapeEluta()),
        asyncio.create_task(scrapeLinkedin()),
        asyncio.create_task(scrapeBebee())
    ]
    # wait for all scraping functions to finish
    await asyncio.gather(*tasks)

    # create table
    table.add_column("Title")
    table.add_column("Company")
    table.add_column("Location")
    table.add_column("Link")
    # loop over dataframe and print rich table
    for index, row in df.iterrows():
        table.add_row(
            f"{row['Title']}",
            f"{row['Company']}",
            f"{row['Location']}",
            f"{row['Link']}",
        )

    console.print(table)


if __name__ == '__main__':
    # run main function
    asyncio.run(main())
