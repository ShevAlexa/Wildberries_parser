from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import telebot
import csv


bot = telebot.TeleBot('1876443989:AAEDggteT3Aj_hVf1Oy60aOCFW1iO-J8Ysc')
chat = 1001584891259
header = ['Name', 'Brand', 'New_price', 'Old_price']

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

search = input('item to search: ')
for letter in search:
    if letter == ' ':
        letter = '%20'
link = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search}'

driver = webdriver.Chrome(desired_capabilities=caps, executable_path='D:\\PyCharm\\IT_OVERONE\\parser\\chromedriver.exe')

while True:
    try:
        driver.get(link)
    except BaseException:
        print('selenium.common.exceptions.WebDriverException')
        continue
    else:
        time.sleep(5)
        break

item = 5   # between 1 and 100
attempts = 0
page = 1

while True:
    if attempts == 3:
        item = 1
        try:
            next_page = driver.find_element(By.XPATH, f'/html/body/div[1]/main'
                                                      f'/div[2]/div/div/div[1]/div[2]/div[2]/div[6]/div/div/a[{page}]')

        except BaseException:
            if attempts == 5:
                break
            page += 1
            item += 1
            attempts += 1
            print('next page not found')
            continue
        else:
            next_page.click()
            attempts = 0
            page += 1
            item = 1
            print('Next Page')

    try:
        new_link = driver.find_element(By.XPATH, f'/html/body/div[1]/'
                                                 f'main/div[2]/div/div/div[1]/div[2]/div[2]/div[5]/div/div/div[{item}]'
                                                 f'/div/a')

    except BaseException:
        item += 1
        attempts += 1
        continue
    else:
        new_link.click()
    time.sleep(5)

    while True:
        try:
            name = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/h1').text
        except BaseException:
            print('fail name')
            problem_link = driver.current_url
            with open('problem_links(old price fail).txt', 'a', encoding='utf-8') as file:
                file.write(f'{problem_link} - (Name fail)\n')
            break

        try:
            new_price = driver.find_element(By.XPATH, '//*[@id="infoBlockProductCard"]/div[2]/div/div/p/span').text
        except BaseException:
            with open('problem_links(old price fail).txt', 'a', encoding='utf-8') as file:
                problem_link = driver.current_url
                file.write(f'{problem_link} - (Price fail)\n')
            break

        try:
            old_price = driver.find_element(By.XPATH, '/html/body/div[1]/main/'
                                                      'div[2]/div/div/div[2]/div/div[3]/div[2]/div/div/p/del').text
        except BaseException:
            with open('problem_links(old price fail).txt', 'a', encoding='utf-8') as file:
                problem_link = driver.current_url
                file.write(f'{problem_link} - (Old price fail)\n')
            bot.send_message(509258928, problem_link)
            break
        else:
            total_price = str()
            for number in new_price:
                if number.isdigit() or total_price == '.':
                    total_price += number

            latest_price = str()
            for number in old_price:
                if number.isdigit() or total_price == '.':
                    latest_price += number

            sale = '{:.0f}'.format(float(total_price) / float(latest_price) * 100)
            sale = 100 - int(sale)
            print(f'{page}. {item} - {name}, {new_price}, {old_price}, {sale}%')

            new_price = str(new_price).replace(' ', '')
            old_price = str(old_price).replace(' ', '')

            product = [name, new_price[:-2], old_price[:-2], str(sale)]

            product = ';'.join(tuple(product)) + '\n'

            with open('links_for_using.csv', "a", encoding="utf-8") as file:
                file.write(product)

            break

    try:
        return_item = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[1]/div[1]/a')
    except BaseException:
        print('return fail')
        driver.get(link)
    else:
        return_item.click()

    item += 1
    time.sleep(10)

# driver.close()

