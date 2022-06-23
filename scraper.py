import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=os.environ.get("GECKODRIVER_PATH"))
while True:
    driver.get("http://results.uoc.ac.in/")
    table = driver.find_element(by="xpath", value='/html/body/span/div[2]/div[1]/div[2]/div/div/div/div[2]/div/table/tbody')
    print(table.get_attribute("innerHTML"))
