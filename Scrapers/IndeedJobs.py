from SimplyHiredJobs import initialize_browser
import re
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import csv


def save_data_to_csv(data, filename):
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Type", "Pay Range", "Description"]
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
    browser.get(job_url)
    # wait for loading the job-page
    time.sleep(2)
    JobHeaderContainer = \
        BeautifulSoup(browser.page_source, 'html.parser').find_all('div', class_='jobsearch-InfoHeaderContainer')[0]

    # Job's location
    location = JobHeaderContainer.find_all_next('div', attrs={'data-testid': 'inlineHeader-companyLocation'})
    if len(location) > 0:
        location = location[0].text
    else:
        try:
            JobInfoContainer = BeautifulSoup(browser.page_source, 'html.parser').find_all('div',
                                                                                          class_='jobsearch-CompanyInfoContainer')[
                0]
            location = JobInfoContainer.find_all_next('div')
            location = location[-1].text
        except:
            location = 'Unknown'

    # Job's pay-range & type
    JobOtherDetails = BeautifulSoup(browser.page_source, 'html.parser').find_all('div', attrs={
        'data-testid': 'jobsearch-OtherJobDetailsContainer'})
    # Verify if JobOtherDetails contains any data, as this may include salary and job type information
    job_salary = None
    job_type = None
    if len(JobOtherDetails) > 0:
        # Extract potential salary and job type information from the first relevant section
        job_info = JobOtherDetails[0].find_all_next('div', attrs={'id': 'salaryInfoAndJobType'})
        if len(job_info) > 0:
            job_info = job_info[0]
            # The extracted job_info typically includes two span elements: one for salary and one for type
            job_info_content_size = len(job_info.contents)
            job_info = job_info.find_all_next('span')

            # If job_info contains exactly two elements, these can be assumed to represent salary and job type
            if job_info_content_size == 2:
                job_salary = job_info[0].text
                job_type = job_info[1].text
            # For a single-element job_info, determine whether it represents salary or type based on its content
            elif job_info_content_size == 1:
                job_info_text = job_info[0].text
                # Presence of '$' indicates that the text corresponds to salary
                if '$' in job_info_text:
                    job_salary = job_info_text
                else:
                    job_type = job_info_text
    # Access the job description container
    JobBodyContainer = \
        BeautifulSoup(browser.page_source, 'html.parser').find_all('div', class_='jobsearch-BodyContainer')[0]
    job_description = JobBodyContainer.find_all_next('div', attrs={'id': 'jobDescriptionText'})
    if len(job_description) > 0:
        # If the job description is found, extract the text
        job_description = job_description[0].text
    else:
        # Assign an empty string if no description is available
        job_description = ""
    # Remove HTML tags (e.g., <p>, <li>) and keep only the plain text content
    # Clean up by trimming leading/trailing spaces and eliminating extra whitespace
    # Replace multiple consecutive newlines with a maximum of two
    job_description = job_description.replace('<p>', '').replace('</p>', '').replace('<li>', '').replace('</li>', '')
    job_description = job_description.replace('<ul>', '').replace('</ul>', '').replace('<ol>', '').replace('</ol>', '')
    job_description = job_description.replace('<div>', '').replace('</div>', '')
    job_description = job_description.strip()
    job_description = re.sub('(\n\n)\n*|\n', r'\1', job_description)

    job_details = {
        'Company': company_name,
        'Job ID': f"job_{job_num}",
        'Job Title': job_title,
        'Job URL': job_url,
        'Location': location,
        'Type': job_type,
        'Pay Range': job_salary,
        'Description': job_description
    }
    # Save the job immediately to CSV
    save_data_to_csv([job_details], filename)
    print(f"Scraped job {job_num}: {job_title}")


def scrape_company_jobs(company, browser, max_runtime, start_time, filename):
    try:
        browser.get(f'https://www.indeed.com/jobs?q={company}')
        time.sleep(2)

        # finding all jobs containers
        try:
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            jobs_containers = soup.find_all('div', class_="job_seen_beacon")
        except:
            print(f"No jobs found for company: {company}")
            return

        job_num = 1
        # keep scraping jobs if there is a next page
        page_num = 1
        while True:
            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                browser.quit()
                break
            # keep the current page in mind to return it after getting all the job's details
            current_page_url = browser.current_url
            for job_container in jobs_containers:
                if time.time() - start_time >= max_runtime:
                    break
                # for every job, let's take the details
                try:
                    fetch_job_details(job_container, browser, job_num, filename)
                except:
                    continue

                # updating the number of jobs
                job_num += 1
            # check for the next page
            browser.get(current_page_url)
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
                        browser.quit()
                        break
                else:
                    print("No next page URL found.")
                    browser.quit()
                    break
            else:
                print("No more pages.")
                browser.quit()
                break

    except Exception as e:
        print(f"Error scraping company jobs: {e}")


if __name__ == "__main__":

    companies_df = pd.read_csv('company_names.csv')
    companies_list = companies_df['name'].tolist()
    # companies_list = companies_list[300:]
    # companies_list = ["Amazon", "Meta", "Nvidia", "Google", "Apple", "Microsoft", "YouTube"]

    # maximum runtime in seconds (10 hours), theoretically, we can scrape for years
    max_runtime = 10 * 60 * 60
    start_time = time.time()

    output_filename = "indeed_jobs_data.csv"
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Type", "Pay Range", "Description"]

    # Create the CSV file with headers if it doesn't exist
    if not os.path.exists(output_filename):
        with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    for company in companies_list:
        browser = initialize_browser()
        if time.time() - start_time >= max_runtime:
            print("Maximum runtime reached. Stopping execution.")
            browser.quit()
            break
        print(f"Starting scraping for: {company}")
        scrape_company_jobs(company, browser, max_runtime, start_time, output_filename)
