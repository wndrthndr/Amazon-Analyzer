from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setup browser
options = Options()
# options.add_argument("--headless")  # Uncomment for silent mode
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(options=options)

driver.get("https://www.amazon.in/s?k=soft+toys")
time.sleep(3)

# Scroll to load more products
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
data = []

for product in products:
    try:
        title = product.find_element(By.TAG_NAME, "h2").text
        url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
        image = product.find_element(By.TAG_NAME, "img").get_attribute("src")

        try:
            brand = product.find_element(By.CLASS_NAME, "a-size-base-plus").text
        except:
            brand = "Unknown"

        try:
            rating_element = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
            rating = rating_element.get_attribute("innerHTML").split()[0]
        except:
         rating = "N/A"


        try:
            reviews = product.find_element(By.CLASS_NAME, "a-size-base").text.replace(",", "")
        except:
            reviews = "0"

        try:
            price = product.find_element(By.CLASS_NAME, "a-price-whole").text.replace(",", "")
        except:
            price = "0"

        data.append({
            "Title": title,
            "Brand": brand,
            "Reviews": reviews,
            "Rating": rating,
            "Price": price,
            "Image URL": image,
            "Product URL": url
        })

    except Exception as e:
        continue

driver.quit()

# Save results
df = pd.DataFrame(data)
df.to_csv("soft_toys_all.csv", index=False)
print(f"✅ Scraped {len(df)} products. CSV saved as soft_toys_all.csv.")
