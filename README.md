# Currency Parsing with Apache Airflow and Docker

**Task Description**
<br/><br/>
Our task is to parse the page https://kurs.kz/ to obtain the highest and lowest currency exchange rates, regardless of the currency type. The goal is to find the maximum and minimum values on the site.
<br/><br/>
### Setup Instructions ###
Use Docker to deploy Apache Airflow:
We will use Docker to set up and run Apache Airflow. Follow these steps to get started:
Download the Docker Compose file for Airflow:

`curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml`

On Linux, the quick-start requires your host user ID and group ID to be set to 0. Otherwise, the files created in **dags**, **logs**, and **plugins** will be owned by the root user. Make sure to configure these for Docker Compose:

`mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env`

Start Airflow using Docker Compose:
`docker-compose up -d`

### Write your Python script ###

This script should parse the website and find the highest and lowest currency exchange rates.
```
import requests
from bs4 import BeautifulSoup

url = "https://kurs.kz/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rates = [float(rate.text) for rate in soup.find_all(class_='some-class')]  # Adjust selector as necessary

max_rate = max(rates)
min_rate = min(rates)

print(f"The most expensive exchange rate: {max_rate}")
print(f"The cheapest exchange rate: {min_rate}")
```

### Save to CSV ###
```
with open('currency_rates.csv', 'w') as file:
    file.write("Max Rate,Min Rate\n")
    file.write(f"{max_rate},{min_rate}\n")
```
    
After running the script, the output will display the highest and lowest exchange rates, and the data will be saved in a CSV file.
![image](https://github.com/user-attachments/assets/00aa64fe-dedf-4a04-a183-fd3a29f5063d)

### Create an Airflow DAG ###

To run the script in Airflow, create a DAG. This is what a DAG looks like:
![image](https://github.com/user-attachments/assets/5265a75c-b618-4af8-80f4-74db978b4cda)

After running the script, the output will display the highest and lowest exchange rates, and the data will be saved in a CSV file.

**Result**
The most expensive exchange rate: 38240
The most cheapest exchange rate: 2.55
