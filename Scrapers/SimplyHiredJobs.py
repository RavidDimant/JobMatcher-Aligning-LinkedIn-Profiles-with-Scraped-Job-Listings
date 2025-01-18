import time
import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def initialize_browser():
    """Initialize the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def get_text(container, tag, attrs):
    """Extract text from a BeautifulSoup tag."""
    try:
        element = container.find(tag, attrs)
        if element:
            return element.text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return ""


def get_qualifications(container):
    """Extract qualifications from the job details."""
    try:
        # Locate the qualifications container
        qualification_section = container.find('div', {'data-testid': 'viewJobQualificationsContainer'})
        if qualification_section:
            # Extract qualification items
            qualifications_list = qualification_section.find_all('span', {'data-testid': 'viewJobQualificationItem'})
            qualifications = [qualification.text.strip() for qualification in qualifications_list]
            # Return the list of qualifications
            return qualifications
    except Exception as e:
        print(f"Error extracting qualifications: {e}")
    return ""


def save_data_to_csv(data, filename):
    """Save data to CSV file."""
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Rate", "Type", "Pay Range", "Qualifications",
                  "Description"]
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for entry in data:
                writer.writerow(entry)
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def fetch_job_details(job_container, browser, job_num, filename):
    """Scrape job details and save them to CSV."""
    try:
        job_link = job_container.find('a', class_="chakra-button css-1djbb1k")
        if job_link:
            job_title = job_link.text.strip()
            job_url = f"https://www.simplyhired.com{job_link['href']}"

            # Visit the job details page
            browser.get(job_url)
            time.sleep(3)

            # Parse job details
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            # Extract job details
            detail_container = soup.find('div', class_="css-s92abg")

            # first, let us scrape the company name - we need to do this explicitly because searching for the company
            # name does not guarantee that the jobs retrieved are actually from the company we searched for
            # in the search bar
            company_name_elements = soup.find_all('span', {'data-testid': 'detailText'})
            if company_name_elements:
                company_name = company_name_elements[0].get_text(strip=True)
            else:
                company_name = ""

            job_details = {
                'Company': company_name,
                'Job ID': f"job_{job_num}",
                'Job Title': job_title,
                'Job URL': job_link['href'],
                'Location': get_text(detail_container, 'span', {'data-testid': 'viewJobCompanyLocation'}),
                'Rate': get_text(detail_container, 'span', {'aria-hidden': 'true', 'class': 'css-0'}),
                'Type': get_text(detail_container, 'span', {'data-testid': 'viewJobBodyJobDetailsJobType'}),
                'Pay Range': get_text(detail_container, 'span', {'data-testid': 'viewJobBodyJobCompensation'}),
                'Qualifications': get_qualifications(detail_container),
                'Description': get_text(detail_container, 'div',
                                        {'data-testid': 'viewJobBodyJobFullDescriptionContent'})
            }

            # Save the job immediately to CSV
            save_data_to_csv([job_details], filename)
            print(f"Scraped job {job_num}: {job_title}")
    except Exception as e:
        print(f"Error fetching job details: {e}")


def scrape_company_jobs(company, browser, max_runtime, start_time, filename):
    """Scrape job listings for a specific company and save each job immediately."""
    try:
        browser.get(f'https://www.simplyhired.com/search?q={company}&l=')
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        jobs_containers = soup.find_all('div', class_="css-obg9ou")

        if not jobs_containers:
            print(f"No jobs found for company: {company}")
            return

        # counting jos for every company
        job_num = 1
        # keep scraping jobs if there is a next page
        page_num = 1
        while True:
            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                break

            for job_container in jobs_containers:
                if time.time() - start_time >= max_runtime:
                    print("Maximum runtime reached. Stopping execution.")
                    break

                # taking more details for jobs
                fetch_job_details(job_container, browser, job_num, filename)
                # updating the number of jobs
                job_num += 1

                # return to the original search results page
                try:
                    # go back to the search results
                    browser.back()
                    # wait for the results page to load
                    time.sleep(3)
                except Exception as e:
                    print(f"Error returning to the results page: {e}")
                    break

            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                break
            # check for the next page
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            next_page_element = soup.find('a', {'aria-label': f'page {page_num + 1}'})
            if next_page_element:
                page_num += 1
                next_page_url = next_page_element.get('href')
                if next_page_url:
                    print(f"Moving to the next page: {next_page_url}")
                    try:
                        browser.get(next_page_url)
                        time.sleep(3)  # Wait for the next page to load
                        jobs_containers = BeautifulSoup(browser.page_source, 'html.parser').find_all('div',
                                                                                                     class_="css-obg9ou")
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
    companies_list = companies_df['name'].to_list()
    # companies_list = ["Amazon", "Meta", "Nvidia", "Google", "Apple", "Microsoft", "YouTube"]

    # maximum runtime in seconds (10 hours), theoretically, we can scrape for years
    max_runtime = 60 * 60 * 10
    start_time = time.time()

    output_filename = "simplyhired_jobs_data.csv"
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Rate", "Type", "Pay Range", "Qualifications",
                  "Description"]

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


