from SimplyHiredJobs import initialize_browser, get_text
import re
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


def save_data_to_csv(data, filename):
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Rate", "Type", "Pay Range", "Description"]
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for entry in data:
                writer.writerow(entry)
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def fetch_job_details(job_container, browser, job_num, filename):
    # "first, let us scrape the company name - we need to do this because searching for the company
    # name does not guarantee that the jobs retrieved are actually from the company we searched for
    # in the search bar"
    company_name_elements = job_container.find_all_next('span', class_="css-1h7lukg eu4oa1w0")
    company_name = company_name_elements[0].get_text(strip=True)

    # Find the job title and its URL
    job_title_box = job_container.find_all_next('h2', class_='jobTitle')
    job_title = job_title_box[0].find_all_next('span')[0].text
    job_url = f'https://www.indeed.com/viewjob?{job_title_box[0].find_all_next("a")[0]["href"].split("?")[1]}'

    # scrape job details
    time.sleep(2)
    details_containers = BeautifulSoup(browser.page_source, 'html.parser').find_all('div',
                                                                                    class_="jobsearch"
                                                                                           "-JobComponent "
                                                                                           "css-1kw92ky "
                                                                                           "eu4oa1w0")
    for detail_container in details_containers:
        # job's description
        JobBodyContainer = BeautifulSoup(browser.page_source, 'html.parser').find_all('div',
                                                                                      class_="jobsearch"
                                                                                             "-BodyContainer css-118ma7z eu4oa1w0")
        if len(JobBodyContainer) == 0:
            continue
        job_description = JobBodyContainer[0].find('div', id='jobDescriptionText')
        if len(job_description) > 0:
            job_description = job_description.text
        else:
            job_description = None
        # removing all kind of unnecessary text and spaces
        job_description = job_description.replace('<p>', '').replace('</p>', '')
        job_description = job_description.replace('<ul>', '').replace('</ul>', '')
        job_description = job_description.replace('<div>', '').replace('</div>', '')
        job_description = job_description.strip()
        job_description = re.sub('(\n\n)\n*|\n', r'\1', job_description)

        time.sleep(1)
        # Locate the parent container by ID
        pay_range = ""
        employment_type = ""
        container = detail_container.find('div', {'data-testid': 'jobsearch-OtherJobDetailsContainer'})
        if container:
            # print("found the parent container")
            # print(container)
            # job's pay range
            pay_range_element = container.find('span', class_="css-1jh4tn2 eu4oa1w0")
            if pay_range_element:
                pay_range = pay_range_element.text.strip()
            # job's employment type
            employment_type_element = container.find('span', class_="css-1h7a62l eu4oa1w0")
            if employment_type_element:
                raw_text = employment_type_element.text.strip()
                employment_type = raw_text.lstrip('-').strip()

        job_details = {
            'Company': company_name,
            'Job ID': f"job_{job_num}",
            'Job Title': job_title,
            'Job URL': job_url,
            'Location': get_text(detail_container, 'div', {'data-testid': "inlineHeader-companyLocation"}),
            'Rate': get_text(detail_container, 'span', {'aria-hidden': 'true', 'class': "css-1g53rkl e1wnkr790"}),
            'Type': employment_type,
            'Pay Range': pay_range,
            'Description': job_description
        }
        # Save the job immediately to CSV
        save_data_to_csv([job_details], filename)
        print(f"Scraped job {job_num}: {job_title}")


def scrape_company_jobs(company, browser, max_runtime, start_time, filename):
    try:
        browser.get(f'https://www.indeed.com/jobs?q={company}')
        time.sleep(3)

        # finding all jobs containers
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        jobs_containers = soup.find_all('div', class_="job_seen_beacon")
        if not jobs_containers:
            print(f"No jobs found for company: {company}")
            return

        job_num = 1
        # keep scraping jobs if there is a next page
        page_num = 1
        while True:
            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                break

            for job_container in jobs_containers:
                if time.time() - start_time >= max_runtime:
                    break

                fetch_job_details(job_container, browser, job_num, filename)

                # updating the number of jobs
                job_num += 1

            # check for the next page
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            next_page_element = soup.find('a', {'aria-label': f'{page_num + 1}'})
            if next_page_element:
                page_num += 1
                next_page_url = next_page_element.get('href')
                if next_page_url:
                    next_page_url = "https://www.indeed.com" + next_page_url
                    print(f"Moving to the next page: {next_page_url}")
                    try:
                        browser.get(next_page_url)
                        # wait for the next page to load
                        time.sleep(3)
                        jobs_containers = BeautifulSoup(browser.page_source, 'html.parser').find_all('div',
                                                                                                     class_="job_seen_beacon")
                    except Exception as e:
                        print(f"Error loading the next page: {e}")
                        break
                else:
                    print("No next page URL found.")
                    break
            else:
                print("No more pages.")
                break

    except Exception as e:
        print(f"Error scraping company jobs: {e}")


if __name__ == "__main__":

    companies_df = pd.read_csv('company_names.csv')
    companies_list = companies_df['name'].tolist()
    # companies_list = companies_list[782:]
    # companies_list = ["Amazon", "Meta", "Nvidia", "Google", "Apple", "Microsoft", "YouTube"]

    # maximum runtime in seconds (10 hours), theoretically, we can scrape for years
    max_runtime = 60 * 60 * 10
    start_time = time.time()

    output_filename = "indeed_jobs_data.csv"
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Rate", "Type", "Pay Range", "Description"]

    # Create the CSV file with headers if it doesn't exist
    if not os.path.exists(output_filename):
        with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    browser = initialize_browser()
    try:
        for company in companies_list:
            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                break
            print(f"Starting scraping for: {company}")
            scrape_company_jobs(company, browser, max_runtime, start_time, output_filename)
    finally:
        browser.quit()




