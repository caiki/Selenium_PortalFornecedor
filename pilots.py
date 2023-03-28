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

url = "https://www.statsf1.com/"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="ctl00_HL_StatsH"]/span').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[1]').click()

pilotos = driver.find_element(By.XPATH, "(//tbody)[2]")
child_elements = pilotos.find_elements(By.XPATH, "tr")

pilotos_info = []
for child_element in child_elements:
    text = child_element.text
    pilotos_info.append((text))

df = pd.DataFrame(columns=['Ranking', 'Name', 'Years', 'Championships'])

for row in pilotos_info:
    row_data = row.split()
    ranking = row_data[0]
    name = row_data[1] + ' ' + row_data[2]
    years = row_data[3:-1]
    championships = row_data[-1]
    df = df.append({'Ranking': ranking, 'Name': name, 'Years': years, 'Championships': championships}, ignore_index=True)

writer = pd.ExcelWriter('pilotos.xlsx', engine='openpyxl')

df.to_excel(writer, sheet_name="pilots_stats", index=False)

writer.save()