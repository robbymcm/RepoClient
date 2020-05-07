# CreateRepo

## Create and clone a GitHub Repository from the command line ##
A python script to login to GitHub, create a repository, and clone the new repository to a specified location

## Dependencies ##
- chromedriver (recommended to have the executable in the project folder or in PATH)
    - A link can be found here: https://chromedriver.chromium.org/ 
- selenium
    - pip install selenium in project folder or virtulenv

## Usage ##
- python3 repo.py <repository_name>
- (optional): python3 repo.py <repository_name> -p (private) || -g (global)

## login.json ##
- Please ensure that you update your username and password for GitHub in login.json
- This file is untracked

## paths.json ##
- path to your version of chromedriver
- path to where you want the new repository to be created; (default is the parent directory)

<br>

Created by: Rob McMahon (6 May, 2020)