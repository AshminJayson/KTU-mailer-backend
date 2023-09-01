import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
# chrome_options.set_capability(
#     "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
# )
chrome_options.add_argument('headless')
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ktu.edu.in/menu/announcements")

# log_entries = driver.get_log('performance')


driver.implicitly_wait(10)
announcements = driver.find_elements(
    by=By.CLASS_NAME, value="col-sm-11")

for announcement in announcements:
    announcement_title = announcement.find_element(
        by=By.TAG_NAME, value="h6").text
    date_of_announcement = announcement.find_element(
        by=By.TAG_NAME, value="div").text
    announcement_content = announcement.find_element(
        by=By.TAG_NAME, value="p").text
    encrypt_id = announcement.find_element(
        by=By.TAG_NAME, value="button").get_attribute("value")

    print(announcement_title, date_of_announcement,
          announcement_content, encrypt_id)
    # break

driver.quit()

# for log_entry in log_entries:
#     network_log = json.loads(log_entry['message'])["message"]

#     if "Network.response" in network_log["method"] or "Network.request" in network_log["method"] or "Network.webSocket" in network_log["method"]:
#         print(network_log)
#         break
