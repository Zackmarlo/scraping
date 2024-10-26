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
driver.get('https://stock.adobe.com/eg/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=0&filters%5Bcontent_type%3Azip_vector%5D=0&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bglobally_safe_collection%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k=interior+design+bathroom&order=relevance&limit=100&search_page=1&search_type=filter-select&acp=&scoring%5Bae_vivid_color%5D=0&color=%23DBDBDB&get_facets=1')

# Create directory to save images if it doesn't exist
save_dir = "bathroom"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

last_file = 0
img_urls = set()  # Use a set to avoid duplicates

def scroll_down():
    """Scroll down the webpage using JavaScript."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def collect_images():
    """Collect image URLs from the current page."""
    images = driver.find_elements(By.TAG_NAME, "picture")
    for img in images:
        try:
            source = img.find_elements(By.TAG_NAME , "source")
            srcset = source[0].get_attribute('srcset')
            # Split the srcset and take the last URL (largest image)
            src = srcset.split(',')[-1].split()[0]
            img_urls.add(src)
        except:
            continue
while len(img_urls) < 200:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)  
    collect_images()
    print(f"Collected {len(img_urls)} images so far...")
    next_page = WebDriverWait(driver , 30).until(
        EC.presence_of_element_located((By.XPATH , '//*[@id="pagination-element"]/nav/span[3]/button'))
    )
    next_page.click()
# Download the images
for img_url in img_urls:
    try:
        filename = f'bathroom_{last_file + 1}.jpg'
        urllib.request.urlretrieve(img_url, os.path.join(save_dir, filename))
        last_file += 1
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

# Quit WebDriver
driver.quit()
