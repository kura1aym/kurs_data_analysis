from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests
from bs4 import BeautifulSoup
import json
import csv

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

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

def download_data():
    url = 'https://kurs.kz/'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve data from {url}. Status code: {response.status_code}")

def parse_data(**context):
    html_content = context['ti'].xcom_pull(task_ids='download_data')
    
    if not html_content:
        raise Exception("No HTML content found from download_data task")
    
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
    
    if punkts_json is None or punkts_from_internet_json is None:
        raise Exception("Failed to parse JSON data from the HTML content")
    
    context['ti'].xcom_push(key='punkts_json', value=punkts_json)
    context['ti'].xcom_push(key='punkts_from_internet_json', value=punkts_from_internet_json)

def save_data_to_csv(**context):
    punkts_json = context['ti'].xcom_pull(task_ids='parse_data', key='punkts_json')
    punkts_from_internet_json = context['ti'].xcom_pull(task_ids='parse_data', key='punkts_from_internet_json')
    
    save_to_csv(punkts_json, '/home/kuralay/kurs_analysis/punkts_data.csv')
    save_to_csv(punkts_from_internet_json, '/home/kuralay/kurs_analysis/punkts_from_internet_data.csv')
    
    print("Data saved to CSV files.")

def calculate_extreme_rates():
    with open('/home/kuralay/kurs_analysis/punkts_data.csv', 'r', encoding='utf-8') as csvfile:
        punkts_data = list(csv.DictReader(csvfile))
    
    with open('/home/kuralay/kurs_analysis/punkts_from_internet_data.csv', 'r', encoding='utf-8') as csvfile:
        punkts_from_internet_data = list(csv.DictReader(csvfile))
    
    all_data = punkts_data + punkts_from_internet_data
    
    max_rate, min_rate = find_extreme_rates(all_data)
    print(f"Highest exchange rate: {max_rate}")
    print(f"Lowest exchange rate: {min_rate}")

with DAG(
    'currency_exchange_analysis',
    default_args=default_args,
    description='A simple DAG to parse currency exchange data and find extreme rates',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
    )

    parse_data_task = PythonOperator(
        task_id='parse_data',
        python_callable=parse_data,
        provide_context=True,
    )

    save_data_to_csv_task = PythonOperator(
        task_id='save_data_to_csv',
        python_callable=save_data_to_csv,
        provide_context=True,
    )

    calculate_extreme_rates_task = PythonOperator(
        task_id='calculate_extreme_rates',
        python_callable=calculate_extreme_rates,
    )

    download_data_task >> parse_data_task >> save_data_to_csv_task >> calculate_extreme_rates_task
