from selenium import webdriver
import json
import sys
import os
import time

## Retrieve data from paths.json
def get_paths():
    with open('paths.json', "r") as f:
        data = json.load(f)
        chrome_path = data['chromedriver']
        repo_path = data['repo_path']
    return (chrome_path, repo_path)


# set paths, create driver
paths = get_paths()
driver = webdriver.Chrome(paths[0])
repo_path = paths[1]


# Dictionary of necessary GitHub element xpaths
driver_links = {
    'url': 'https://github.com/login',
    'username': 'login_field',
    'password': 'password',
    'sign_in_btn': 'commit',
    'new_btn': '/html/body/div[4]/div/aside[1]/div[2]/div[2]/div/h2/a',                 # by xpath onwards
    'repo_name': '/html/body/div[4]/main/div/form/div[2]/auto-check/dl/dd/input',
    'public': '/html/body/div[4]/main/div/form/div[3]/div[1]/label/input',
    'private': '/html/body/div[4]/main/div/form/div[3]/div[2]/label/input',
    'readme': '/html/body/div[4]/main/div/form/div[3]/div[4]/div[1]/label/input[2]',
    'create_btn': '/html/body/div[4]/main/div/form/div[3]/button',
    'clone_btn': '/html/body/div[4]/div/main/div[2]/div/div[3]/span/get-repo-controller/details/summary',
    'copy_link': '/html/body/div[4]/div/main/div[2]/div/div[3]/span/get-repo-controller/details/div/div/div[1]/div[1]/div/input'
}

# Errors
errors = {
    'E_REPO_NAME': 'Usage: repo.py <repository_name>',
    'E_PERMISSIONS': 'Please choose either: `-p` for private or `-g` for global'
}


## Retrieve login data from `login.json`
## @returns - tuple (username, password)
def get_login_data():
    with open('login.json', "r") as f:
        data = json.load(f)
        user_name = data['username']
        password = data['password']
    if user_name == "" or password == "":
        print("Please enter your username and password")
        exit()
    return (user_name, password)


## Process command line arguments
## @returns - tuple (name, permission)
def get_repo_name():
    name = ""
    permission = "-p"
    permissions = ["-p", "-g"]

    # repo name
    if len(sys.argv) == 1:
        print(errors['E_REPO_NAME'])
        exit()
    else:
        name = sys.argv[1]
    
    # permissions
    if len(sys.argv) == 3:
        if sys.argv[2] not in permissions:
            print(errors['E_PERMISSIONS'])
            exit()
        elif sys.argv[2] == permissions[1]:
            permission = "-g"

    return (name, permission)


## Login to github.com
def login():
    login_info = get_login_data()

    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(login_info[0])
    driver.find_element_by_id('password').send_keys(login_info[1])
    driver.find_element_by_name('commit').click()


## Create repo
## @returns - link to newly created repo
def create_repo(name, permission):
    driver.find_element_by_xpath(driver_links['new_btn']).click()
    driver.find_element_by_xpath(driver_links['repo_name']).send_keys(name)
    if permission == '-p':
        driver.find_element_by_xpath(driver_links['private']).click()

    driver.find_element_by_xpath(driver_links['readme']).click()
    time.sleep(0.5)
    driver.find_element_by_xpath(driver_links['create_btn']).click()
    driver.find_element_by_xpath(driver_links['clone_btn']).click()

    # get value of the WebElement, split and take text after last space for repo link
    link = driver.find_element_by_xpath(driver_links['copy_link']).get_property('value')
    link = link.split(" ")[-1]

    return link


## Clone the repo after changing directory to repo_path
def clone_repo(link):
    os.chdir(repo_path)

    command = "git clone " + link
    os.system(command)


if __name__ == "__main__":
    repository = get_repo_name()
    login()
    link = create_repo(repository[0], repository[1])
    clone_repo(link)
    driver.close()