import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


# Search for jobs on stepstone.de with all concerning keywords and parameters
# Paste url of search results here:
search_url = "https://www.stepstone.de/5/ergebnisliste.html?rsearch=1&ke=data%20scientist&action=facet_selected%3Bexperiences%3B90001&ex=90001"


# Function for parsing search sites and extracting links to job ads
# Creates a list of links.
def extract_href(page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0)Gecko/20100101 Firefox/100.0"}
    url = search_url + f"&of={page}"
    search_page = requests.get(url, headers)
    soup_search = BeautifulSoup(search_page.text, "html.parser")
    search_results = soup_search.find_all("div", {"class": "Wrapper-sc-11673k2-0 fpBevf"})

    for job in search_results:
        href_url.append(job.find("a", {"class": "sc-pAZqv cyGFEN"})["href"])
    sleep(3)
    return href_url


# Each Stepstone search site contains 25 job ads
# To browse multiple sites range(0, 450, 25) has to be adjusted
# E.g. range(0, 25, 25) parses one search site or up to 25 job ads
# range(0, 50, 25) parses two search sites or up to 50 jobs etc.
href_url = []
for i in range(0, 50, 25):
    extract_href(i)
    print("Scraping links of " + str(len(href_url)) + " data science job ads.")

print(str(len(href_url)) + " job ads found.")


# Function for parsing individual job site to gather detailed information
# Creates a list of dics (one dic per job)
# Each dic contains title, company name, location, employment and position type and detailed content of the job offer
def extract_jobs(href):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    job_url = "https://www.stepstone.de" + href
    job_page = requests.get(job_url, headers)
    job_soup = BeautifulSoup(job_page.content, "html.parser")

    try:
        job_title = job_soup.find("h1", {"class": "listing__job-title at-header-company-jobTitle sc-jDwBTQ fiXdfY"}).text.replace("\n", " ")
    except AttributeError:
        job_title = "None"
    try:
        company_name = job_soup.find("a", {"class": "at-listing-nav-company-name-link at-header-company-name sc-jAaTju eOAenU sc-cMljjf kwCDeT"}).text
    except AttributeError:
        company_name = "None"
    try:
        location = job_soup.find("li", {"class": "at-listing__list-icons_location js-map-offermetadata-link sc-chPdSV jStOTt"}).text
    except AttributeError:
        location = "None"
    try:
        employment = job_soup.find("li", {"class": "at-listing__list-icons_contract-type sc-chPdSV jStOTt"}).text
    except AttributeError:
        employment = "None"
    try:
        position_type = job_soup.find("li", {"class": "at-listing__list-icons_work-type sc-chPdSV jStOTt"}).text
    except AttributeError:
        position_type = "None"
    try:
        job_content = job_soup.find("div", {"class": "js-app-ld-ContentBlock"}).text.replace("\n", " ")
    except AttributeError:
        job_content = "None"

    job = {
        "job_title": job_title,
        "company_name": company_name,
        "location": location,
        "employment": employment,
        "position_type": position_type,
        "job_content": job_content
        }

    job_list.append(job)
    sleep(3)
    return job_list


job_list = []
for href in href_url:
    extract_jobs(href)
    print("Scraped " + str(len(job_list)) + " job ads.")


# Creating a .csv table of all the scraped jobs and saving it locally
df = pd.DataFrame(job_list)
df.to_csv("data_science_jobs.csv")
