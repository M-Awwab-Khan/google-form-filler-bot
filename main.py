import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import *

response = requests.get(ZILLOW_LINK)
soup = BeautifulSoup(response.text, 'html.parser')

prices = [price.text.split('+')[0].split('/')[0] for price in soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')]
addresses = [address.text.strip().replace('| ', '') for address in soup.find_all('address')]
links = [link.get('href') for link in soup.find_all('a', 'StyledPropertyCardDataArea-anchor')]

pal = zip(addresses, prices, links)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)
for address, price, link in pal:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))).send_keys(address)
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(price)
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(link)
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div').click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Submit another response'))).click()