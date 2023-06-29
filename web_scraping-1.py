# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:23:26 2023

@author: pierr
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time 

driver = webdriver.Chrome("chromedriver")
driver.set_page_load_timeout(10)
driver.get("https://www.truecar.com/used-cars-for-sale/listings/")
driver.set_page_load_timeout(30)



data = []
curr_min = 0
curr_max = 2000

df = pd.DataFrame(columns=['year', 'model', 'price', 'mileage', 'location', 'condition', 'id'])

while curr_max <= 100000:
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div/div[2]/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div/div[2]/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/input").send_keys(curr_min)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div/div[2]/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div/div[2]/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/input").send_keys(curr_max)
    
    time.sleep(5)
    while True:
        cars_infos = driver.find_elements(By.CLASS_NAME, "vehicle-card-body")
        for car in cars_infos:
            car_details = []
            year = car.find_element(By.CLASS_NAME, "vehicle-card-year")
            model = car.find_element(By.CLASS_NAME, "truncate")
            price = car.find_elements(By.CLASS_NAME, "font-bold")[-1]
            mileage = car.find_elements(By.CLASS_NAME, "truncate")
            location = car.find_element(By.CLASS_NAME, "vehicle-card-location")
            condition = car.find_elements(By.CLASS_NAME, "vehicle-card-location")[2]
            vin = car.find_element(By.CLASS_NAME, "vehicle-card-vin-carousel-challenger")
            car_details.append(year.text)
            car_details.append(model.text)
            car_details.append(price.text)
            if mileage[-2].text == "Upfront Price Available":
                car_details.append(mileage[-3].text)
            else:
                car_details.append(mileage[-2].text)
            car_details.append(location.text) 
            car_details.append(condition.text)
            car_details.append(vin.text)
            data.append(car_details)
            
        try:
            next_page = driver.find_element(By.XPATH , '//*[@data-test="Pagination-directional-next"]')
        except:
            break
        
        next_page_link = next_page.get_attribute("href")
        driver.get(next_page_link)
    
    
    df_curr = pd.DataFrame(data, columns = ['year', 'model', 'price', 'mileage', 'location', 'condition', 'id'])
    df = df.append(df_curr, ignore_index=True)
    curr_min = curr_max + 1
    curr_max = curr_max + 1000

df.to_csv("C:/Users/pierr/Documents/OneDrive - University of Toronto/year 3/ECO481/up10k.csv")

