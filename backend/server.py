from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from chromedriver_py import binary_path

#Production Imports
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from flask import Flask, jsonify

import time
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

app = Flask(__name__)

#Initial Request
@app.route("/")
def running():
    return "<p>Server is Running :)</p>"

#Login
@app.route("/login")
def login():
    try:
        #Scraper Settings
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        if os.getenv('app_env') == 'production':
            svc = webdriver.ChromeService(ChromeDriverManager().install())
            browser = webdriver.Chrome(options=chrome_options, service=svc)
        else:
            svc = webdriver.ChromeService(executable_path=binary_path)
            browser = webdriver.Chrome(options=chrome_options, service=svc)

        #Accessing Instagram and Logging In
        print("Starting: /login")

        browser.get("https://www.instagram.com/")
        print("Opened Browser")

        username_input = WebDriverWait(browser, 6).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input'))
            )
        ActionChains(browser)\
            .send_keys_to_element(username_input, os.getenv('email'))\
            .perform()
        print("Entered Email")
        
        password_input = WebDriverWait(browser, 6).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div/label/input'))
            )
        ActionChains(browser)\
            .send_keys_to_element(password_input, os.getenv('password'))\
            .perform()
        print("Entered Password")

        login_button =  WebDriverWait(browser, 6).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[3]'))
            )
        ActionChains(browser)\
            .click(login_button)\
            .perform()
        print("Pressed Login")
        
        time.sleep(5)
        browser.get('https://www.instagram.com/web/search/topsearch/?query=find.my.opps')

        response_element = WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/pre"))
        )
        print("Login Succesful!")
        response = json.loads(response_element.text)
        return response
    except Exception as error:
        response = {'status': 400, 'message': str(error)}
        return jsonify(response)

if __name__ == '__main__':
    app.run()