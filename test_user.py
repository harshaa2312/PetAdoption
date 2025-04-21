from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class UserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = Service('./chromedriver.exe')
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.maximize_window()
        cls.driver.get("http://127.0.0.1:5000/")
        time.sleep(2)
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def wait_and_find(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def test_1_user_login_and_adopt_pet(self):
        driver = self.driver

        # Login as user
        self.wait_and_find(By.NAME, "email").send_keys("harshaa@gmail.com")
        self.wait_and_find(By.NAME, "password").send_keys("123")
        self.wait_and_find(By.NAME, "role").send_keys("User")
        self.wait_and_find(By.XPATH, '//button[contains(text(), "Login")]').click()
        print("✅ User login successful!")
        time.sleep(2)
        # Go to View Available Pets
        self.wait_and_find(By.LINK_TEXT, "View Available Pets").click()
        time.sleep(2)

        # Click first Adopt button
        adopt_buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[contains(text(), "Adopt")]'))
        )
        if adopt_buttons:
            adopt_buttons[0].click()
            print("✅ Adopt button clicked!")
        else:
            print("❌ No pets available to adopt.")
            return
        time.sleep(2)
        # Fill Adoption Form
        self.wait_and_find(By.NAME, "name").send_keys("Harsha H")
        self.wait_and_find(By.NAME, "email").send_keys("user1@gmail.com")
        self.wait_and_find(By.NAME, "phone").send_keys("9876543210")
        self.wait_and_find(By.NAME, "address").send_keys("123, Park Street, City")
        self.wait_and_find(By.NAME, "reason").send_keys("I love pets and want to give them a loving home.")
        form_element = self.wait_and_find(By.NAME, "name")  # Using any form field to locate the form
        form_element.submit()
        print("✅ Adoption form submitted successfully!")
        time.sleep(2)
        # Handle popup alert
        WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for alert
        alert = driver.switch_to.alert
        print(f"⚡ Alert says: {alert.text}")
        alert.accept()  # Accept the alert
        print("✅ Alert closed successfully.")
        time.sleep(2)
        # Wait for the page to load after redirect
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
        )
        time.sleep(2)

        # Click Logout
        self.wait_and_find(By.LINK_TEXT, "Logout").click()
        print("👋 User logged out successfully.")
        time.sleep(2)
        # Close the browser window
        driver.quit()
        print("✅ Browser closed.")

if __name__ == "__main__":
    unittest.main()
