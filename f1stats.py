# Import necessary libraries

import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import openpyxl
from datetime import date

# Set URL for the Formula 1 stats website
url = "https://www.statsf1.com/"

# Initialize Chrome webdriver and navigate to the website
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# Wait for website to load
time.sleep(1)

# Click on the "Stats" button in the top menu
driver.find_element(By.XPATH, '//*[@id="ctl00_HL_StatsH"]/span').click()

# Wait for the "Stats" menu to load, then click on "Numbers" link
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[1]').click()

# Scrape data from the "Pilots" table
pilotos = driver.find_element(By.XPATH, "(//tbody)[2]")
child_elements = pilotos.find_elements(By.XPATH, "tr")

pilotos_info = []
for child_element in child_elements:
    text = child_element.text
    pilotos_info.append((text))

# Convert scraped data into a pandas DataFrame
df = pd.DataFrame(columns=['Ranking', 'Name', 'Years', 'Championships'])

for row in pilotos_info:
    row_data = row.split()
    ranking = row_data[0]
    name = row_data[1] + ' ' + row_data[2]
    years = row_data[3:-1]
    championships = row_data[-1]
    df = df.append({'Ranking': ranking, 'Name': name, 'Years': years, 'Championships': championships}, ignore_index=True)

# Save DataFrame to an Excel file using openpyxl engine
writer = pd.ExcelWriter('pilotos.xlsx', engine='openpyxl')
df.to_excel(writer, sheet_name="pilots_stats", index=False)
writer.save()

# Print success message and close webdriver
print("Data successfully scraped and saved to 'pilotos.xlsx'!")
driver.quit()