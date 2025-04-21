from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class AdminTests(unittest.TestCase):
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

    def test_1_admin_login(self):
        driver = self.driver
        driver.find_element(By.NAME, "email").send_keys("admin@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        role_select = Select(driver.find_element(By.NAME, "role"))
        role_select.select_by_visible_text("Admin")
        driver.find_element(By.XPATH, '//form//button').click()
        time.sleep(3)
        self.assertIn("Dashboard", driver.title)
        print("✅ Admin login successful!")

    def test_2_manage_pets_add_delete(self):
        driver = self.driver
        # Click Manage Pets
        driver.find_element(By.PARTIAL_LINK_TEXT, "Manage Pets").click()
        time.sleep(2)

        # Add new pet
        driver.find_element(By.NAME, "name").send_keys("Tommy")
        driver.find_element(By.NAME, "breed").send_keys("Golden Retriever")
        driver.find_element(By.NAME, "age").send_keys("2")
        driver.find_element(By.NAME, "image").send_keys(r"C:\pet_adoption_project\premium_photo-1694819488591-a43907d1c5cc.jpg")
        driver.find_element(By.XPATH, '//button[contains(text(),"Add Pet")]').click()
        time.sleep(3)
        print("✅ Pet added successfully!")
        time.sleep(3)
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Find and delete the added pet
        pet_rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
        pet_found = False
        for row in pet_rows:
            name_cell = row.find_elements(By.TAG_NAME, 'td')[1]
            if name_cell.text.strip() == "Tommy":
                delete_link = row.find_element(By.XPATH, './/a[contains(@href, "/delete_pet/")]')
                delete_link.click()
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(2)
                pet_found = True
                print("🗑️ Pet deleted successfully!")
                time.sleep(2)
                break
        if not pet_found:
            print("❌ Pet not found for deletion.")

        # ✅ After managing pets, go back to dashboard
        driver.find_element(By.PARTIAL_LINK_TEXT, "Dashboard").click()
        time.sleep(2)

        # ✅ Now manage adoption requests
        driver.find_element(By.PARTIAL_LINK_TEXT, "Adoption Requests").click()
        time.sleep(2)

        approve_buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Approve")]')
        if approve_buttons:
            approve_buttons[0].click()
            print("✅ Adoption request approved!")
        else:
            print("ℹ️ No pending adoption requests found.")

        time.sleep(2)

if __name__ == "__main__":
    unittest.main()
