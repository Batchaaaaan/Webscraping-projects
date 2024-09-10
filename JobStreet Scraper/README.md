# JobStreet Scraper
This is a Web scraping project that extracts job posting from https://www.jobstreet.com.ph.

### Features
-  It utilizes Python libraries such as BeautifulSoup for parsing HTML content and Requests for handling HTTP requests to extract key information from job listings, such as job titles, companies, locations, and job descriptions.
-  The collected data is then organized and cleaned for better usability.
-  The resulting dataset can be exported and downloaded as a CSV file, making it suitable for further analysis.

### Information Extracted
The following are the information extracted while using the scraper:
- Job title
- Company Name
- Company Location
- Work Arrangement(if remote)
- Salary
- Benefits
- Listing Date
- Date of Extraction
- Job Posting URL

Note: Not all information have data on it since some fields in the website are not supplied.

### Tools
- Python  
  Python Library Used:
  - BeautifulSoup
  - requests
  - os
  - datetime
  - time
  - csv
  
