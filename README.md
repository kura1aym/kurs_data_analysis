<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Parsing with Apache Airflow and Docker</title>
</head>
<body>
    <h1>Currency Parsing with Apache Airflow and Docker</h1>
    
    <h2>Task Description</h2>
    <p>Our task is to parse the page <a href="https://kurs.kz/">https://kurs.kz/</a> to obtain the highest and lowest currency exchange rates, regardless of the currency type. The goal is to find the maximum and minimum values on the site.</p>
    
    <h2>Setup Instructions</h2>
    
    <h3>Airflow with Docker</h3>
    
    <ol>
        <li><strong>Use Docker to deploy Apache Airflow:</strong>
            <p>We will use Docker to set up and run Apache Airflow. Follow these steps to get started:</p>
            <ol>
                <li>Download the Docker Compose file for Airflow:</li>
                <pre><code>curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml'</code></pre>
                <li>On Linux, the quick-start requires your host user ID and group ID to be set to 0. Otherwise, the files created in <code>dags</code>, <code>logs</code>, and <code>plugins</code> will be owned by the root user. Make sure to configure these for Docker Compose:</li>
                <pre><code>mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env</code></pre>
                <li>Start Airflow using Docker Compose:</li>
                <pre><code>docker-compose up -d</code></pre>
            </ol>
        </li>
        <li><strong>Write your Python script:</strong>
            <p>Place your script in the <code>scripts</code> directory. This script should parse the website and find the highest and lowest currency exchange rates.</p>
            <h4>Example Script</h4>
            <pre><code>import requests
from bs4 import BeautifulSoup

url = "https://kurs.kz/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rates = [float(rate.text) for rate in soup.find_all(class_='some-class')]  # Adjust selector as necessary

max_rate = max(rates)
min_rate = min(rates)

print(f"The most expensive exchange rate: {max_rate}")
print(f"The cheapest exchange rate: {min_rate}")

# Save to CSV
with open('currency_rates.csv', 'w') as file:
    file.write("Max Rate,Min Rate\n")
    file.write(f"{max_rate},{min_rate}\n")</code></pre>
        </li>
    </ol>
    
    <h2>Output</h2>
    <p>After running the script, the output will display the highest and lowest exchange rates, and the data will be saved in a CSV file.</p>
    <pre><code>The data is saved in a CSV file.
СThe most expensive exchange rate: 38240
The cheapest exchange rate: 2.55</code></pre>
    
    <img src="![image](https://github.com/user-attachments/assets/e398d9ae-751f-4d03-b06b-0f6fd1815471)
" alt="Output Example">
    
    <h2>Notes</h2>
    <ul>
        <li>Make sure you have Docker and Docker Compose installed on your machine.</li>
        <li>The class selector <code>.some-class</code> in the BeautifulSoup parser should be adjusted according to the actual HTML structure of the target website.</li>
    </ul>
    
    <h2>Conclusion</h2>
    <p>By following these steps, you will be able to parse the currency exchange rates from the specified website and identify the highest and lowest rates using Apache Airflow and Docker.</p>
</body>
</html>
