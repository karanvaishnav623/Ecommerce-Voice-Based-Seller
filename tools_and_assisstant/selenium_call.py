from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def specific_product_info(link):
    # Set up the Selenium WebDriver (e.g., using Chrome)
    driver = webdriver.Chrome()  # Make sure you have the correct WebDriver installed

    # Open the link
    driver.get(link)

    try:
        # Wait for the element with the specific class to load (up to 10 seconds)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/p/']"))
        )

        # Extract and return the page source or specific element text
        return driver.page_source
    finally:
        # Close the browser
        driver.quit()


print(specific_product_info(
    "https://www.flipkart.com/mobile/compare?ids=MOBGYT2HEYWFCG8Q,MOBHYFPPYRCQZMHG"))
