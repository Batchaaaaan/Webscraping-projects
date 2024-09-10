from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import random
import csv

        
def get_record(job):
    def get_job_title():
        job_title = job.find('a', {'data-testid': 'job-card-title'}).text
        return job_title
    
    def get_company():
        company = job.find('a', {'data-type': 'company'})
        if company:
            job_company = job.find('a', {'data-type': 'company'}).text
        else:
            job_company = 'Private Advertiser'
        return job_company
    
    def get_location():
        job_location = job.find('a', {'data-type': 'location'}).text
        return job_location
    
    def get_listing_date():
        listing_date = job.find('span', {'data-automation': 'jobListingDate'}).text
        return listing_date
        
    def get_url():
        url = 'https://www.jobstreet.com.ph' + job.find('a', {'data-automation': 'job-list-view-job-link'}).get('href')
        return url
    
    def get_work_arrangement():
        job_arrangement_tag = job.find('span', {'data-testid': 'work-arrangement'})
        if job_arrangement_tag:
            is_remote = 'Y'
        else:
            is_remote = 'N'
        return is_remote
    
    def get_benefits():
        job_benefits_tag = [package.text for package in job.find_all('li')]
        if job_benefits_tag:
            job_benefits = job_benefits_tag
        else:
            job_benefits = ''
        return job_benefits
    
    def get_salary():
        salary_tag = job.find('span', {'data-automation': 'jobSalary'})
        if salary_tag:
            job_salary = salary_tag.text.strip()
        else:
            job_salary = ''
        return job_salary
    

    date_today = datetime.today().strftime('%Y-%m-%d')
    
        
        #compile into a single set
    record = (get_job_title(), get_company(), get_location(), get_work_arrangement(), get_salary(), get_benefits(), get_listing_date(), date_today, get_url())
    return record
    
def get_url():
    position = input('What position are your applying for?')
    location = input('Where is your preferred location?').strip()
    
    if location:
        template = 'https://www.jobstreet.com.ph/{}-jobs/in-{}'
    else:
        template = 'https://www.jobstreet.com.ph/{}-jobs'

    position = position.replace(' ', '-')
    location = location.replace(' ', '-')
    url = template.format(position, location)
    return url
        
def run():
    global records
    records = []
    url = get_url()
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html')
        jobs = soup.find_all('article', {'data-testid':'job-card'})

        for job in jobs:
            record = get_record(job)
            records.append(record)

        try:
            url = 'https://www.jobstreet.com.ph' + soup.find('a', {'title': 'Next'}).get('href')
        except:
            break

        print('running....')
        time.sleep(random.randint(0,5)) #put the code to sleep to avoid server being flooded
    return 'All records retrieved' 

def print_records():
    #print records
    return records

def get_length():
    #returns the total number of jobs
    return len(records)

def save_records(file_name='results.csv'):
    path = r"C:\Users\HP\Downloads\\" + file_name
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['JobTitle', 'Company', 'Location', 'is_remote', 'Salary', 'Benefits', 'listing_date', 'date_parsed', 'URL'])
        writer.writerows(records)
    return 'File successfully saved'