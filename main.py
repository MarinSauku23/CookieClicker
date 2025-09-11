from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url="https://ozh.github.io/cookieclicker/")

# Wait for page to load
sleep(3)

# Handle initial popups (cookies consent does not have to be clicked, but language does)
print("Looking for language selection...")

try:
    # Select English language
    language_button = driver.find_element(By.ID, value="langSelect-EN")
    print("Found language button, clicking...")
    language_button.click()
    sleep(3) # More loading
except NoSuchElementException:
    print("Language selection not found")

# Wait for everything to settle
sleep(2)

# Find the big cookie to click
big_cookie = driver.find_element(By.ID, value="bigCookie")

# Set timers
wait_time = 5
timeout = time() + wait_time  # Check for purchases every 5 seconds
five_min = time() + 60 * 5  # Run for 5 min

while True:
    big_cookie.click()

    # Every 5 seconds, try to buy the most expensive item we can afford
    if time() > timeout:
        try:
            # Get current cookie count
            cookies_element = driver.find_element(By.ID, value="cookies")
            cookie_text = cookies_element.text

            # Extract number from text like "1 cookie"
            cookie_count = int(cookie_text.split()[0].replace(",", ""))

            # Find all available products in the store
            products = driver.find_elements(By.CSS_SELECTOR, value="#products .enabled")

            # Find the most expensive item we can afford
            most_expensive_item = None
            for product in reversed(products): # Start from most expensive
                # Check if item is available and affordable (enabled class)
                if "enabled" in product.get_attribute("class"):
                    most_expensive_item = product
                    break

            # Buy the most expensive item if found
            if most_expensive_item is not None:
                most_expensive_item.click()
                print(f"Bought item: {most_expensive_item.get_attribute('id')}")
        except (NoSuchElementException, ValueError):
            print("Couldn't find cookie count or items.")

        # Reset timer
        timeout = time() + wait_time

    # Stop after 5 minutes
    if time() > five_min:
        try:
            cookies_element = driver.find_element(By.ID, value="cookies")
            print(f"Final result: {cookies_element.text}")
        except NoSuchElementException:
            print("Couldn't get final cookie count")
        finally:
            driver.close()
        break
