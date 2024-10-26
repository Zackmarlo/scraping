import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

# Set up Edge WebDriver
edge_driver_path = 'webdriver/msedgedriver.exe'  # Replace with your Edge WebDriver path
options = Options()

service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# Go to Google Images and search for a keyword
driver.get('https://www.beautifulhomes.asianpaints.com/interior-design-ideas/bedroom.html')

last_file = 2683
save_dir = "downloads"

img_urls = set()
load_more = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "gallery_btn"))
)


while load_more:
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more)
        time.sleep(2)
        load_more.click()
        time.sleep(2)
        load_more = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "gallery_btn"))
        )
    except:
        break

images = driver.find_elements(By.XPATH, "//img[contains(@class, 'gallery-room-img')]")
print(len(images))
for img in images[238:]:
    try:
        src = img.get_attribute('src')
        img_urls.add(src)
    except:
        continue

for img_url in img_urls:
    try:
        urllib.request.urlretrieve(img_url, os.path.join(save_dir, f'bedroom_{last_file + 1}.jpg'))
        last_file += 1
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")


driver.quit()
