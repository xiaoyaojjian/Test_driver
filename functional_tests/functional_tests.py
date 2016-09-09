from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('http://192.168.3.84:8090/')
time.sleep(30)
assert 'Django' in browser.title
print(browser.title)
browser.quit()