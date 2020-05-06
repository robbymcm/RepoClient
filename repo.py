from selenium import webdriver
import json

driver = webdriver.Chrome('/Users/robert/Desktop/current/CreateRepo/chromedriver')

def get_login_data():
    with open('login.json', "r") as f:
        data = json.load(f)
        user_name = data['username']
        password = data['password']
    return (user_name, password)


## Login to github.com
def login():
    login_info = get_login_data()

    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(login_info[0])
    driver.find_element_by_id('password').send_keys(login_info[1])
    driver.find_element_by_name('commit').click()

login()