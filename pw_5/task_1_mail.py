from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# под win executable_path не указываю
driver = webdriver.Chrome()
driver.get('https://account.mail.ru/login')


def authorization(arg):
    arg.implicitly_wait(5)
    enter_login = arg.find_element(By.XPATH, "//input[@name='username']")
    enter_login.send_keys('pentegov_92')
    arg.implicitly_wait(5)
    button_enter = arg.find_element(By.XPATH, "//span[text()='Ввести пароль']")
    button_enter.click()
    arg.implicitly_wait(5)
    enter_pass = arg.find_element(By.XPATH, "//input[@name='password']")
    enter_pass.send_keys('121212qwer')
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
        print(res_set)
        action = ActionChains(driver)
        action.move_to_element(message[-1])
        action.perform()
        scroll(res_set)


def parse(links):
    result_list = []
    result = {}
    for link in links:
        driver.get(link)
        driver.implicitly_wait(10)
        result['from'] = driver.find_element(By.XPATH,
                                             "//div[@class='letter__author']/span[@class='letter-contact']/text()")
        result['time'] = driver.find_element(By.XPATH, "//div[@class='letter__date']/text()")
        result['title'] = driver.find_element(By.XPATH, "//h2[@class='thread-subject']/text()")
        result['content'] = driver.find_element(By.XPATH, "//div[contains(@class,'body-content')]").text
        driver.implicitly_wait(60)
    return result


authorization(driver)


