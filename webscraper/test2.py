from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://bananarepublic.gapcanada.ca/browse/category.do?cid=44873&nav=meganav%3AMen%3AMen%27s%20Clothing%3ACasual%20Shirts")

imgs = driver.find_element_by_tag_name('img')
print(imgs)
# for img in imgs:
#     try:
#         img.screenshot('./images'+'/clothing (' +
#                        img.get_attribute('alt') + ').png')
#         time.sleep(0.2)
#     except:
#         continue

driver.save_screenshot("screenshot.png")

driver.close()
