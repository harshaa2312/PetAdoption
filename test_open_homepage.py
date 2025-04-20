from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://localhost:5000/")  # or whatever URL you want to open
print("Title of page is:", driver.title)

driver.quit()
