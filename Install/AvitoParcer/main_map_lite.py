import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from math import ceil
from func_export_to_xlsx import export_to_xlsx

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

os.system('pause')

os.system('cls')

#os.system('mode 199, 50')

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

for i in elm_prop:
    print(i.text)
print(elm_prop)

count_e = 1
for e in elm_prop:
    print(f"Загрузка объектов: {count_e}/{len(elm_prop)}")
    name = e.find_element(By.CLASS_NAME, 'styles-link-cQMwi').get_attribute('title')
    link = e.find_element(By.CLASS_NAME, 'styles-link-cQMwi').get_attribute('href')
    price = e.find_element(By.CLASS_NAME, 'styles-module-root-bLKnd').text.split(' ')
    print(price)
    price = f"{price[0]}{price[1]}"
    try:
        addr = e.find_element(By.CLASS_NAME, 'styles-module-noAccent-LowZ8').text
    except selenium.common.exceptions.NoSuchElementException:
        addr = e.find_element(By.CLASS_NAME, 'styles-module-noAccent-l9CMS').text
    print(f'Name: {name} | Link: {link} | Addr: {addr}')
    rent_object = {
        'Name': name,
        'Price': int(price),
        'Address': addr,
        'Link': link
    }
    objects.append(rent_object)
    count_e = count_e + 1

# for i in elm_prop:
#     try:
#         print('Count: ', count)
#         try:
#             price = find_price(browser=browser, url_search=f'{table_links[count]}?guests=2&calendar=true') # Поиск цены объекта
#         except IndexError:
#             print('File main_map.py | Stroke 93 | Error!')
#             continue
#         if price == False:
#             print(price)
#             count = count + 1
#             continue
#         print(price)
#         # Составление архитектуры объекта
#         rent_object = {
#             'Name': table_txt[count],
#             'Price': price,
#             'Address': table_addr[count],
#             'Link': table_links[count]
#         }
#         # Добавление объекта в список
#         objects.append(rent_object)
#         print(rent_object)
#         print('======================================================================================================================================================================================================')
#         count = count + 1
#     except selenium.common.exceptions.StaleElementReferenceException:
#         continue


for i in objects:
    print(i)

# Создание xlsx таблицы

namefile = input('Введите имя файла (без .xlsx): ')

export_to_xlsx(objects=objects, namefile=namefile)

browser.close()

print('Работа завершена! Можно закрывать программу.')