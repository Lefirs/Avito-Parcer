import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
import os

def find_price(browser, url_search):
    browser.get(url_search) # Поиск указанной ссылки
    try:
        browser.find_element(By.CLASS_NAME, 'firewall-title') # Проверка блокировки IP
        print('Строка 12: Ошибка! Возможно вышла капча.')
        os.system('pause')
    except selenium.common.exceptions.NoSuchElementException:
        exce = True
    time.sleep(1)
    dontbookingrent = browser.find_elements(By.CLASS_NAME, 'styles-module-hoverable-_XDVD') # Проверка на незабронированные ячейки
    if not dontbookingrent:
        return False

    dontbookingrent[0].click()
    dontbookingrent = browser.find_elements(By.CLASS_NAME, 'styles-module-hoverable-_XDVD') # Проверка на незабронированные ячейки
    dontbookingrent[0].click()

    time.sleep(1)

    priceget = browser.find_elements(By.CLASS_NAME, 'styles-module-size_xxxl-GRUMY') # Получение цены квартиры

    try:
        price1 = priceget[1].text.split(' ')[0] # Соединение цены ( Вычет пробелов из цены )
        price2 = priceget[1].text.split(' ')[1] # Соединение цены ( Вычет пробелов из цены )
    except AttributeError:
        print('Строка 36: Ошибка! Возможно не прогружен элемент цены.')
        os.system('pause')
        price1 = priceget[1].text.split(' ')[0]
        price2 = priceget[1].text.split(' ')[1]
    price = f'{price1}{price2}'
    return int(price)