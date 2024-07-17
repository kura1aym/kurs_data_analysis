import requests
from bs4 import BeautifulSoup
import json
import csv

def save_to_csv(data, filename):
    if not data:
        print(f"No data to save for {filename}")
        return
    
    keys = data[0].keys()  
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def find_extreme_rates(data):
    all_rates = []
    for entry in data:
        for currency, rates in entry['data'].items():
            if rates[0] != 0 and rates[1] != 0:
                all_rates.extend(rates)
                
    max_rate = max(all_rates)
    min_rate = min(all_rates)
    return max_rate, min_rate

url = 'https://kurs.kz/'

response = requests.get(url, verify=False)

if response.status_code == 200:
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    scripts = soup.find_all('script')
    
    punkts_json = None
    punkts_from_internet_json = None
    
    for script in scripts:
        script_text = script.string
        if script_text:
            if 'var punkts = [' in script_text:
                start_index = script_text.find('var punkts = ') + len('var punkts = ')
                end_index = script_text.find(';', start_index)
                punkts_data = script_text[start_index:end_index].strip()
                punkts_json = json.loads(punkts_data)
            
            if 'var punktsFromInternet = [' in script_text:
                start_index = script_text.find('var punktsFromInternet = ') + len('var punktsFromInternet = ')
                end_index = script_text.find(';', start_index)
                punkts_from_internet_data = script_text[start_index:end_index].strip()
                punkts_from_internet_json = json.loads(punkts_from_internet_data)
    
    save_to_csv(punkts_json, 'punkts_data.csv')
    save_to_csv(punkts_from_internet_json, 'punkts_from_internet_data.csv')

    print("Данные сохранены в CSV файлы.")
    
    all_data = punkts_json + punkts_from_internet_json
    
    max_rate, min_rate = find_extreme_rates(all_data)
    print(f"Самый дорогой курс: {max_rate}")
    print(f"Самый дешевый курс: {min_rate}")

else:
    print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
