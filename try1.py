import smtplib
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium WebDriver
s = Service("C:/Users/HP/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Navigate to the Cisco publication listing page
driver.get("https://sec.cloudapps.cisco.com/security/center/publicationListing.x")

# Wait for the element to be clickable, then click
try:
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/cdc-template/div[2]/div[4]/div[1]/div[2]/div[1]/div[2]/table/tbody[2]/tr[1]/td/table/tbody/tr[1]/td[1]/div/span[4]/a"))
    )
    element.click()
except Exception as e:
    print(f"Error: {e}")
    driver.quit()
    exit()

# Wait for the page to load completely
time.sleep(10)  # You can replace this with another WebDriverWait if needed

# Extract the product name
product_name = driver.find_element(By.XPATH, "/html/body/cdc-template/table/tbody/tr/td/table/tbody/tr/td/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div[2]").text

# Extract the reporting date
reporting_date = driver.find_element(By.XPATH, "/html/body/cdc-template/table/tbody/tr/td/table/tbody/tr/td/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/div[2]").text

# Extract the version number
version_number = driver.find_element(By.XPATH, "/html/body/cdc-template/table/tbody/tr/td/table/tbody/tr/td/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div[3]/div[1]").text

# Extract all Cisco Bug IDs and their associated links
bug_ids_elements = driver.find_elements(By.CSS_SELECTOR, "div.ddtsList div.bugDiv a")
bug_ids = [(bug.text, bug.get_attribute("href")) for bug in bug_ids_elements]

# Extract the CVSS score
cvss_score = driver.find_element(By.XPATH, "/html/body/cdc-template/table/tbody/tr/td/table/tbody/tr/td/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div[7]/div[2]/div/input").get_attribute("value")

# Format the email content
email_content = f"""
Product Name: {product_name}
Reporting Date: {reporting_date}
Version Number: {version_number}
CVSS Score: {cvss_score}

Bug IDs and Links:
"""

for bug_id, link in bug_ids:
    email_content += f"{bug_id}: {link}\n"

# Set up the SMTP server and send the email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('sender id', 'sender id pswd')

# Send the email
server.sendmail(
    'ssrane_b21@ce.vjti.ac.in',
    'ranesahil472@gmail.com',
    email_content
)
print("Email sent successfully!")

# Close the SMTP server
server.quit()

# Wait for manual input before closing the browser
# input("Press Enter to continue...")

# Close the browser
driver.quit()
