from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup ChromeDriver
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:5000/")

wait = WebDriverWait(driver, 10)

email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
email_input.send_keys("harshaa@gmail.com")
time.sleep(1)
password_input = driver.find_element(By.NAME, "password")
password_input.send_keys("123")
time.sleep(1)
# Wait for button by type=submit
login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
login_button.click()
time.sleep(1)
print("Login Test Completed.")
driver.quit()
