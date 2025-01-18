from SimplyHiredJobs import initialize_browser, get_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


def save_data_to_csv(data, filename):
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Type", "Pay Range", "Skills", "Description"]
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for entry in data:
                writer.writerow(entry)
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def scrape_company_jobs(company, browser, max_runtime, start_time, filename):
    try:
        browser.get(f'https://www.dice.com/jobs?q={company}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&language=en')
        time.sleep(3)

        # save the main window handle
        main_window = browser.window_handles[0]

        # check if the time limit has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_runtime:
            print("Maximum runtime reached. Exiting loop.")
            browser.quit()
            return

        # Main loop to iterate over all pages
        while True:
            # check if the time limit has been exceeded
            elapsed_time = time.time() - start_time
            if elapsed_time >= max_runtime:
                print("Maximum runtime reached. Exiting loop.")
                break
            # try:
            #     WebDriverWait(browser, 10).until(
            #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="search-card"]'))
            #     )
            # except Exception as e:
            #     print(f"Error loading the job containers: {e}")
            #     break

            # Get all job cards on the current page
            jobs_containers = browser.find_elements(By.CSS_SELECTOR, '[data-cy="search-card"]')
            if len(jobs_containers) == 0:
                print(f"No jobs for the company {company}")
                break

            job_num = 1
            for job_container in jobs_containers:
                # check if the maximum runtime has been exceeded
                if time.time() - start_time >= max_runtime:
                    print("Maximum runtime reached. Stopping execution.")
                    browser.quit()
                    break
                try:
                    # "first, let us scrape the company name - we need to do this because searching for the company
                    # name does not guarantee that the jobs retrieved are actually from the company we searched for
                    # in the search bar"
                    soup = BeautifulSoup(job_container.get_attribute('outerHTML'), 'html.parser')
                    company_name_element = soup.find('a', {'data-cy': 'search-result-company-name'})
                    company_name = company_name_element.get_text(strip=True)

                    # Find and click on the job link
                    job_link = job_container.find_element(By.CSS_SELECTOR, 'a[data-cy="card-title-link"]')
                    job_title = job_link.text.strip()
                    job_link.click()

                    # Switch to the new job detail tab
                    WebDriverWait(browser, 10).until(lambda d: len(browser.window_handles) > 1)
                    browser.switch_to.window(browser.window_handles[-1])
                    time.sleep(3)  # Ensure the page is loaded

                    job_url = browser.current_url
                    soup = BeautifulSoup(browser.page_source, 'html.parser')

                    # Get skills
                    skills_container = soup.find('div', {'data-cy': 'skillsList'})
                    skills = [skill.text.strip() for skill in skills_container.find_all('span', id=lambda
                        x: x and x.startswith('skillChip:'))] if skills_container else []

                    # Get job description
                    job_description_element = soup.find('div', {'data-testid': 'jobDescriptionHtml'})
                    job_description = ' '.join(job_description_element.get_text(separator=' ', strip=True).split()) if job_description_element else ""

                    job_details = {
                        'Company': company_name,
                        'Job ID': f"job_{job_num}",
                        'Job Title': job_title,
                        'Job URL': job_url,
                        'Location': get_text(soup, 'li', {'data-cy': 'location'}),
                        'Type': get_text(soup, 'span', {'id': lambda x: x and x.startswith('employmentDetailChip:')}),
                        'Pay Range': get_text(soup, 'span', {'id': lambda x: x and x.startswith('payChip:')}),
                        'Skills': skills,
                        'Description': job_description
                    }
                    # Save the job immediately to CSV
                    save_data_to_csv([job_details], filename)
                    print(f"Scraped job {job_num}: {job_title}")

                    # updating the number of jobs
                    job_num += 1
                    # check if the maximum runtime has been exceeded
                    if time.time() - start_time >= max_runtime:
                        print("Maximum runtime reached. Stopping execution.")
                        browser.quit()
                        break

                except Exception as e:
                    print(f"Error processing job {job_num}: {e}")
                finally:
                    # Close the job detail tab and switch back to the main search page
                    browser.close()
                    browser.switch_to.window(main_window)

            # check if the maximum runtime has been exceeded
            if time.time() - start_time >= max_runtime:
                print("Maximum runtime reached. Stopping execution.")
                browser.quit()
                break
            # Check for the next page
            try:
                next_page_button = browser.find_element(By.CSS_SELECTOR,
                                                        '[aria-label="Next page"][data-testid="pageNumberBlockNext"]')
                next_page_button.click()
                time.sleep(3)  # Wait for the next page to load
            except Exception as e:
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

    output_filename = "dice_jobs_data.csv"
    fieldnames = ["Company", "Job ID", "Job Title", "Job URL", "Location", "Type", "Pay Range", "Skills", "Description"]

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
