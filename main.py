# web scraping
import time

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

# instantiate global variables
df = pd.DataFrame(columns=['Title', 'Location',
                  'Company', 'Link', 'Description'])
console = Console()
table = Table(show_header=True, header_style="bold")

# get user input
console.print("Enter Job Title :", style="bold green", end=" ")
inputJobTitle = input()
console.print("Enter Job Location :", style="bold green", end=" ")
inputJobLocation = input()


async def scrapeJobDescription(url):
    global df

    driver = DriverOptions()

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        jobDescription = soup.find(
            "div", class_="show-more-less-html__markup").text.strip()
        return jobDescription
    except:
        return ""


def DriverOptions():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    return driver


async def scrapeLinkedin():
    global df
    global inputJobTitle
    global inputJobLocation

    driver = DriverOptions()

    counter = 0
    pageCounter = 1

    while True:
        try:
            driver.get(
                f"https://www.linkedin.com/jobs/search/?&keywords={inputJobTitle}&location={inputJobLocation}&refresh=true&start={counter}")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            ulElement = soup.find('ul', class_='jobs-search__results-list')
            liElements = ulElement.find_all('li')

            for item in track(liElements, description=f"Linkedin - Page: {pageCounter}"):
                jobTitle = item.find(
                    'h3', class_='base-search-card__title').text.strip()
                jobLocation = item.find(
                    'span', class_='job-search-card__location').text.strip()
                jobCompany = item.find(
                    "h4", class_="base-search-card__subtitle").text.strip()
                jobLink = item.find_all("a")[0]['href']

                jobDescription = await scrapeJobDescription(jobLink)

                if jobTitle and jobLocation and jobCompany and jobLink:
                    df = pd.concat([df, pd.DataFrame({'Title': [jobTitle], 'Location': [
                        jobLocation], 'Company': [jobCompany], 'Link': [
                        jobLink], 'Description': [jobDescription]})])

            console.print("Scrape Next Page? (y/n) :",
                          style="bold yellow", end=" ")
            continueInput = input()

            if continueInput == "n":
                break

            counter += 25
            pageCounter += 1

        except:
            break

    driver.quit()


async def main():
    await scrapeLinkedin()

    # create table
    table.add_column("Title")
    table.add_column("Company")
    table.add_column("Location")
    table.add_column("Link")
    table.add_column("Description")
    # loop over dataframe and print rich table
    for index, row in df.iterrows():
        table.add_row(
            f"{row['Title']}",
            f"{row['Company']}",
            f"{row['Location']}",
            f"{row['Link']}",
            f"{(row['Description'])[:20]}..."
        )

    console.print(table)


if __name__ == '__main__':
    # run main function
    asyncio.run(main())
