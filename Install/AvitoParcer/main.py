import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
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


# Применение настроек - > старт
browser = webdriver.Chrome(options=chrome_options)
browser.get(url_search)

print('Закройте окно "Заселения и выезда"')

os.system('pause')

os.system('cls')

os.system('mode 199, 50')

objects = [] # Инициализация списка объектов

try:
    browser.find_element(By.CLASS_NAME, 'firewall-title') # Проверка блокировки IP
    print('Строка 25: Ошибка! Возможно вышла капча.')
    os.system('pause')
except selenium.common.exceptions.NoSuchElementException:
    print('Старт работы программы.')

count = 0


elm_table = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div[3]/div[3]/div[4]/div[2]") # Поиск списка объектов
elm_prop = elm_table.find_elements(By.CLASS_NAME, "iva-item-root-_lk9K") # Поиск объектов в списке
table_txt = [] # Список отвечающий за названия и адреа объектов
table_links = [] # Список отвечающий за ссылки на объекты
for e in elm_prop:
    table_txt.append(e.text)
    table_links.append(e.find_element(By.CLASS_NAME, 'styles-module-root-iSkj3').get_attribute('href'))

for i in elm_prop:
    try:
        name = table_txt[count].split('\n')[0]
        address = table_txt[count].split('\n')[3]
        price = find_price(browser=browser, url_search=f'{table_links[count]}?guests=2&calendar=true') # Поиск цены объекта
        if price == False:
            continue
        # Составление архитектуры объекта
        rent_object = {
            'Name': name,
            'Price': price,
            'Address': address,
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