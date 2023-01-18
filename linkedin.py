from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3432268149&f_AL=true&geoId=104116203&keywords=java%20developer&location=Seattle%2C%20Washington%2C%20United%20States&refresh=true")

username = "colbyleed@yahoo.com"
password = "Luna22!#"

sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(username)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)
time.sleep(2)
all_listings = driver.find_elements(
    By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    time.sleep(2)
    try:
        apply_button = driver.find_element(
            By.CSS_SELECTOR, ".job-s-apply buton")
        apply_button.click()
        time.sleep(2)
        phone = driver.find_element(
            By.CSS_SELECTOR, "fb-single-line-text__input")
        phone.send_keys("2065387716")
        next_button = driver.find_element(By.CSS_SELECTOR, "footer button")
        next_button.click()
        time.sleep(2)
        review_button = driver.find_element(
            By.CLASS_NAME, "artdeco-button--primary")
        if review_button.get_attribute("data-control0name") == "continue_unify":
            close_button = driver.find_element(
                By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_element(
                By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex Application, skipped...")
        else:
            review_button.click()
            time.sleep(2)
            submit_button = driver.find_element(
                By.CLASS_NAME, "artdeco-button--primary")
            if submit_button.get_attribute("data-control-name") == "submit_unify":
                submit_button.click()
                time.sleep(2)
                close_button = driver.find_element(
                    By.CLASS_NAME, "artdeco-modal__dismiss")
                close_button.click()
            else:
                close_button = driver.find_element(
                    By.CLASS_NAME, "artdeco-modal__dismiss")
                close_button.click()
                time.sleep(2)
                discard_button = driver.find_element(
                    By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
                discard_button.click()
                print("Complex Application, skipped...")
                continue
    except NoSuchElementException:
        print("No application button, skipped")
        continue

# driver.close()
