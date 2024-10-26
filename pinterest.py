from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import urllib.request

# Edge WebDriver setup
options = Options()
options.add_argument("--disable-features=SmartScreen")  # Disable SmartScreen
driver = webdriver.Edge(service=Service('D:\\python lessons\\Data Science\\interior design\\webdriver\\msedgedriver.exe'), options=options)

# Open Pinterest page
driver.get('https://uk.pinterest.com/kellyroque1970/white-living-rooms/')

# Create directory to save images if it doesn't exist
save_dir = "living"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

last_file = 0
img_urls = set()  # Use a set to avoid duplicates

def scroll_down():
    """Scroll down the webpage using JavaScript."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def collect_images():
    """Collect image URLs from the current page."""
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        try:
            src = img.get_attribute('src')
            if src and src.startswith('http'):  # Only collect valid URLs
                img_urls.add(src)
        except:
            continue
# Scroll and collect images until we have 1000 images
while len(img_urls) < 100:
    scroll_down()
    time.sleep(1)  # Allow time for new images to load
    collect_images()
    print(f"Collected {len(img_urls)} images so far...")

# Download the images
for img_url in img_urls:
    try:
        urllib.request.urlretrieve(img_url, os.path.join(save_dir, f'bedroom_{last_file}.jpg'))
        last_file += 1
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

# Quit WebDriver
driver.quit()
