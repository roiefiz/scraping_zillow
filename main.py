from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# set up the webdriver
driver = webdriver.Chrome()

# navigate to the Zillow website
driver.get("https://www.zillow.com/")

# search for Detroit, MI
search_box = driver.find_element(By.ID, "search-box-input")
search_box.send_keys("Detroit, MI")
search_box.send_keys(Keys.RETURN)

# wait for the search results to load
time.sleep(5)

# filter for properties that are up for sale and cost less than $450,000 USD
for_sale_filter = driver.find_element(By.XPATH, "//button[@data-value='true']")
for_sale_filter.click()

price_filter = driver.find_element(By.XPATH, "//input[@aria-label='Price']")
price_filter.click()
price_filter.send_keys("$0")
price_filter.send_keys(Keys.TAB)
price_filter.send_keys("$450,000")
price_filter.send_keys(Keys.RETURN)

# wait for the filtered search results to load
time.sleep(5)

# scrape the filtered search results
properties = driver.find_elements("//div[@class='list-card-info']")
for prop in properties:
    price = prop.find_element_by_xpath(".//div[@class='list-card-price']")
    if '$' in price.text and 'M' not in price.text:  # filter out non-numeric prices and prices in millions
        price_num = int(price.text.replace('$', '').replace(',', ''))
        if price_num < 450000:  # filter for properties that cost less than $450,000
            address = prop.find_element_by_xpath(".//address")
            print(address.text, '-', price.text)

# close the webdriver
driver.quit()
