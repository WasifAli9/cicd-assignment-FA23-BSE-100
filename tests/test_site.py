import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8090")


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-data-dir=/tmp/chrome-profile")
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    yield drv
    drv.quit()


def test_page_title(driver):
    driver.get(BASE_URL)
    assert driver.title == "CI/CD Assignment FA23-BSE-100"


def test_main_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading")
    assert "FA23-BSE-100" in heading.text


def test_button_shows_message(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Hello")
    )
    assert driver.find_element(By.ID, "message").text == "Hello from the CI/CD pipeline!"
    driver.save_screenshot("screenshot.png")


def test_textbox_submit_echo(driver):
    driver.get(BASE_URL)
    box = driver.find_element(By.ID, "user-input")
    box.clear()
    box.send_keys("Assignment3 works")
    driver.find_element(By.ID, "submit-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "echo"), "Assignment3 works")
    )
    assert driver.find_element(By.ID, "echo").text == "Assignment3 works"
