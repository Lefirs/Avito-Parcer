import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from math import ceil
from func_export_to_xlsx import export_to_xlsx
from func_find_price import find_price

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

print('Закройте окно "Заселения и выезда", если оно присутствует.')

#os.system('pause')

os.system('cls')

os.system('mode 199, 50')

objects = []

try:
    browser.find_element(By.CLASS_NAME, 'firewall-title') # Проверка блокировки IP
    print('Строка 41: Ошибка! Возможно вышла капча.')
    os.system('pause')
except selenium.common.exceptions.NoSuchElementException:
    print('Старт работы программы.')

count = 0
try:
    count_objects_in_table = int(browser.find_element(By.CLASS_NAME, 'breadcrumbs-count-tSv33').text)
except selenium.common.exceptions.NoSuchElementException:
    count_objects_in_table = int(browser.find_element(By.CLASS_NAME, 'breadcrumbs-count-JteSh').text)

print(ceil(count_objects_in_table / 10))

#class_atr = browser.find_element(By.CLASS_NAME, "#app > div > div.styles-singlePageWrapper-eKDyt > div > div.index-map-mb3Ax > div > div > div.side-block-root-fK4W5 > div > div.styles-root-Q2aLw").get_attribute('class')

for i in range(0, count_objects_in_table):
    try:
        browser.execute_script(f"document.getElementsByClassName('styles-root-CJb8Z')[0].scrollTop = document.getElementsByClassName('styles-root-CJb8Z')[0].scrollHeight")
    except selenium.common.exceptions.JavascriptException:
        browser.execute_script(f"document.getElementsByClassName('styles-root-Q2aLw')[0].scrollTop = document.getElementsByClassName('styles-root-Q2aLw')[0].scrollHeight")
    time.sleep(1)

try:
    elm_table = browser.find_element(By.CLASS_NAME, "styles-container-Abd7K") # Поиск списка объектов
except selenium.common.exceptions.NoSuchElementException:
    elm_table = browser.find_element(By.CLASS_NAME, "styles-container-vFt7G")
elm_prop = elm_table.find_elements(By.CLASS_NAME, "styles-snippet-DBv3Q") # Поиск объектов в списке

print(elm_prop)

table_txt = [] # Список отвечающий за названия объектов
table_addr = [] # Список отвечающий за адреса объектов
table_links = [] # Список отвечающий за ссылки на объекты
for e in elm_prop:
    name = e.find_element(By.CLASS_NAME, 'styles-link-cQMwi').get_attribute('title')
    link = e.find_element(By.CLASS_NAME, 'styles-link-cQMwi').get_attribute('href')
    addr = e.find_element(By.CLASS_NAME, 'styles-module-noAccent-LowZ8').text
    print(f'Name: {name} | Link: {link} | Addr: {addr}')
    table_txt.append(name)
    table_links.append(link)
    table_addr.append(addr)

print('links: ', table_links)

for i in elm_prop:
    try:
        print('Count: ', count)
        try:
            price = find_price(browser=browser, url_search=f'{table_links[count]}?guests=2&calendar=true') # Поиск цены объекта
        except IndexError:
            print('File main_map.py | Stroke 93 | Error!')
            continue
        if price == False:
            print(price)
            count = count + 1
            continue
        print(price)
        # Составление архитектуры объекта
        rent_object = {
            'Name': table_txt[count],
            'Price': price,
            'Address': table_addr[count],
            'Link': table_links[count]
        }
        # Добавление объекта в список
        objects.append(rent_object)
        print(rent_object)
        print('======================================================================================================================================================================================================')
        count = count + 1
    except selenium.common.exceptions.StaleElementReferenceException:
        continue

# Создание xlsx таблицы

namefile = input('Введите имя файла (без .xlsx): ')

export_to_xlsx(objects=objects, namefile=namefile)

browser.close()

print('Работа завершена! Можно закрывать программу.')