import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
from constants import *

response = requests.get(ZILLOW_LINK)
soup = BeautifulSoup(response.text, 'html.parser')

prices = [price.text.split('+')[0].split('/')[0] for price in soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')]
addresses = soup.find_all('address')
links = soup.find_all('a', 'StyledPropertyCardDataArea-anchor')

print(prices)