from bs4 import BeautifulSoup
import requests
import time
import random
import datetime
import csv

def get_links():
    results = []
    url = 'https://www.autodeal.com.ph/used-cars/search/certified-pre-owned+repossessed+used-car-status/page-1?sort-by=relevance'
    print('getting links...')
    while True:
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html')
            extracted_results = soup.find('div', id='results-view')
            cars = extracted_results.find_all('article')
        else:
            break
        

        for car in cars:
            link = car.a.get('href')
            results.append(link)

        try:
            url = soup.find('a', class_='positionabsolute darklink next-button paginator-page').get('href')
        except:
            break

        time.sleep(random.randint(0,3))
    return results
            
def get_data(url):
    url = 'https://www.autodeal.com.ph' + url
    rdict = dict()
    record = []
    response = requests.get(url)
    try:
        if response.ok:
            soup = BeautifulSoup(response.content, 'html')
            location = soup.find('div', {'id': 'sellerprofile'}).find('p', class_='microcopy')
            date_posted = soup.find('div', class_='sellersubinfo textleft').text.strip()[-10:]
            date_now = datetime.datetime.now()
            year = soup.find('h1').text[:4]
            
            if location:
                location = location.text
            else:
                location = soup.find('div', {'id': 'sellerprofile'}).find('span', class_='microcopy').text
            spec_table = ['keydetails', 'features', 'safety']
            rdict['Location'] = location
            rdict['DatePosted'] = date_posted
            rdict['DateNow'] = date_now
            rdict['Year'] = year
            for spec in spec_table:
                data = soup.find('div', {'id': f'{spec}'}).find_all('div')
                for index, y in enumerate(data):
                    if index % 2 == 0:
                        text = y.text.strip().replace(' ', '').replace('\n', '').replace('n/a', '')
                        rdict[text] = data[index+1].text.strip()
    
        else:
            print(response)

    except:
        print(Exception)
        pass
    record_table = ['Price', 'Make', 'Model', 'Year', 'Variant', 'BodyType','EngineSize', 'Transmission', 'FuelType', 'Mileage', 'NumberofDoors',
                    'Location', 'DatePosted', 'DateNow', 'CruiseControl', 'LeatherUpholstery', 'PushStart', 'AirConditioning', 'EntertainmentSystem',
                    'Airbag:Driver', 'Airbag:FrontPassenger', 'Airbag:Side', 'Airbag:Curtain', 'Airbag:Knee', 'ABS', 'Immobilizer', 'SecurityAlarm']

    for feature in record_table:
        if feature in rdict:
            record.append(rdict[feature])
        else:
            record.append('')
        
    return record

def run(file_name='results.csv'):
    records = []
    
    all_results = get_links()

    print('running...')
    for result in all_results:
        record = get_data(result)
        records.append(record)

    path = r"C:\Users\HP\Downloads\\" + file_name
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Price', 'Make', 'Model', 'Year', 'Variant', 'BodyType','EngineSize', 'Transmission', 'FuelType', 'Mileage', 'Number of Doors',
                    'Location', 'DatePosted', 'DateNow', 'CruiseControl', 'LeatherUpholstery', 'PushStart', 'AirConditioning', 'EntertainmentSystem',
                    'Airbag:Driver', 'Airbag:FrontPassenger', 'Airbag:Side', 'Airbag:Curtain', 'Airbag:Knee', 'ABS', 'Immobilizer', 'SecurityAlarm'])
        writer.writerows(records)
        
    return f'Finished running, Data saved in {path}.'