import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from math import ceil
from func_export_to_xlsx import export_to_xlsx
from func_find_price import find_price
from main import rent_object

# Инициализация ссылки
url_search = input('Введите URL: ')

# Инициализация настроек браузера
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--log-level=3")

# Немного рекламы
print("""
Git: https://github.com/Lefirs
""")

time.sleep(1)
os.system('cls')

browser = webdriver.Chrome(options=chrome_options)
browser.get(url_search)

try:
    elm_table = browser.find_element(By.CLASS_NAME, "styles-container-Abd7K") # Поиск списка объектов
except selenium.common.exceptions.NoSuchElementException:
    elm_table = browser.find_element(By.CLASS_NAME, "styles-container-vFt7G")
elm_prop = elm_table.find_elements(By.CLASS_NAME, "styles-snippet-DBv3Q") # Поиск объектов в списке

