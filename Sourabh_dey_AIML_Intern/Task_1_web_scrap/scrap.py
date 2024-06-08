import os
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse

import pandas as pd
import csv



def auto_scroll(driver):
    scroll_pause_time = 2  # Adjust to your needs
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


        
# Function to generate LinkedIn job search URL
def generate_linkedin_url(job_title, country, company=None, job_type=None, experience_level=None, location=None, remote=None):
    base_url = "https://www.linkedin.com/jobs/search"
    params = {
        "keywords": job_title,
        "location": country,
        "trk": "public_jobs_jobs-search-bar_search-submit"
    }
    if company:
        params["f_C"] = company
    if job_type:
        params["f_JT"] = job_type
    if experience_level:
        params["f_E"] = experience_level
    if location:
        params["f_L"] = location
    if remote:
        params["f_RM"] = remote
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def extract_job_info(html_content):
    job_listings = []
    job_cards = html_content.find_elements(By.CLASS_NAME, 'result-card')
    for job_card in job_cards:
        job_title = job_card.find_element(By.CLASS_NAME, 'job-card-search__title').text
        company_name = job_card.find_element(By.CLASS_NAME, 'job-card-container__company-name').text
        job_location = job_card.find_element(By.CLASS_NAME, 'job-card-search__location').text
        job_link = job_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        job_listings.append([job_title, company_name, job_location, job_link])
    return job_listings

def clean_job_count(count_str):
    # Remove non-numeric characters except for digits and commas
    clean_str = ''.join(filter(lambda x: x.isdigit() or x == ',', count_str))
    return int(clean_str.replace(',', ''))


def generate_google_search_url(query):
    base_url = "https://www.google.com/search"
    params = {
        "q": query
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"



if __name__ == '__main__':

    
    job_title = input("Input Job Title: ").strip()
    country = input("Enter Job Location/Country: ").strip()
    company = input("Enter Company Name (optional): ").strip() or None
    job_type = input("Enter Job Type (optional): ").strip() or None
    experience_level = input("Enter Experience Level (optional): ").strip() or None
    location = input("Enter Location (optional): ").strip() or None
    remote = input("Enter Remote Status (optional): ").strip() or None
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
    edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
    edge_service = Service(edge_driver_path)
    edge_options = Options()
    edge_options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Edge(service = edge_service, options = edge_options)


    try:
        browser.get(generate_linkedin_url(job_title, country))
        #browser.get('https://www.linkedin.com/jobs/data-analytics-jobs/?currentJobId=3918709990&originalSubdomain=in')
        # Handle "Open App" or "Continue" option
        try:
            continue_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
            continue_button.click()
        except:
            pass

        # Wait until the job count element is present
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'results-context-header__job-count'))
        )
            
            # Get the job count
        count = browser.find_element(By.CLASS_NAME, 'results-context-header__job-count').text
        count_num = clean_job_count(count)
        print(f"Total jobs found: {count_num}")

        print(f"Total jobs found: {count_num}")

        auto_scroll(browser)

        # Perform auto-scrolling
        auto_scroll(browser)
        time.sleep(10)
        
        # Fetch the page source after scrolling
        html_content = browser.page_source

        print(html_content)
        job_listings = []
        job_cards = browser.find_elements(By.CLASS_NAME, 'job-card-container')
        for job_card in job_cards:
            job_title = job_card.find_element(By.CLASS_NAME, 'job-card-search__title').text
            company_name = job_card.find_element(By.CLASS_NAME, 'job-card-container__company-name').text
            job_location = job_card.find_element(By.CLASS_NAME, 'job-card-search__location').text
            job_link = job_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            job_listings.append([job_title, company_name, job_location, job_link])

        #print(job_listings)
        # Store the job listings in a CSV file
        csv_filename = "linkedin_jobs.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Job Title', 'Company Name', 'Location'])
            csv_writer.writerows(job_listings)
        
        print(f"Job listings saved to {csv_filename}")
        
        ch1 = input("Go to Generalised search?(y/n): ").strip()
        if ch1 == 'y':
            search_query = input("Enter the search item")
            browser.get(generate_google_search_url(search_query))

            # Wait until search results are loaded
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'search'))
            )

            auto_scroll(browser)

            search_results = extract_search_results(browser)

            # Store the search results in a CSV file
            csv_filename = "google_search_results.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Title', 'Link', 'Snippet'])
                csv_writer.writerows(search_results)

            print(f"Search results saved to {csv_filename}")
        else:
            pass

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ch = input("Close or not?(y/n) :").strip().lower()
        if ch in  ['y','Y']:
            browser.quit()
            #exit()
        else:
            pass

