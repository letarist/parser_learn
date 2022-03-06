from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Установил линукс, буду привыкать теперь

# s = Service('./chromedriver')
# driver = webdriver.Chrome(service=s)
driver = webdriver.Chrome(
    ChromeDriverManager().install())  # Проверил - так тоже работает, но ругается на то, что внутри этого объекта используется executible_path
driver.get('https://account.mail.ru/login')


def authorization(arg):
    arg.implicitly_wait(5)
    enter_login = arg.find_element(By.XPATH, "//input[@name='username']")
    enter_login.send_keys(YOU_EMAIL)
    arg.implicitly_wait(5)
    button_enter = arg.find_element(By.XPATH, "//span[text()='Ввести пароль']")
    button_enter.click()
    arg.implicitly_wait(5)
    enter_pass = arg.find_element(By.XPATH, "//input[@name='password']")
    enter_pass.send_keys(YOU_PASSWORD)
    button_enter = arg.find_element(By.XPATH, "//span[text()='Войти']")
    button_enter.click()
    scroll()


def scroll(res_set=None):
    if res_set is None:
        res_set = set()
    message = driver.find_elements(By.XPATH, '//a[contains(@class,"js-letter-list-item")]')
    link_message = [i.get_attribute('href') for i in message]
    if link_message[-1] in res_set:
        return parse(res_set)
    else:
        res_set.update(link_message)
        action = ActionChains(driver)
        action.move_to_element(message[-1])
        action.perform()
        scroll(res_set)


def parse(links):
    result_list = []
    result = {}
    for link in links:
        try:
            driver.get(link)
            driver.implicitly_wait(10)
            result['_id'] = link
            result['from'] = driver.find_element(By.CLASS_NAME, 'letter-contact').text
            result['time'] = driver.find_element(By.CLASS_NAME, 'letter__date').text
            result['title'] = driver.find_element(By.CLASS_NAME, 'thread-subject').text
            result['content'] = driver.find_element(By.XPATH, "//div[contains(@class,'body-content')]").text
            driver.implicitly_wait(60)
            result_list.append(result)
            write_to_db(result_list)
        except (NoSuchElementException, InvalidArgumentException):
            pass

    driver.close()


def write_to_db(result):
    client = MongoClient()
    email_info = client['info_email']
    item = email_info.item
    for res in result:
        try:
            item.insert_one(res)
        except DuplicateKeyError:
            pass


authorization(driver)
