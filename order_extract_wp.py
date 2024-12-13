import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Setup the WebDriver with the local ChromeDriver path
chrome_driver_path = r'C:\Users\Pratyusha Chatterjee\Downloads\chromedriver-win64(1)\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code
print("Please scan the QR code to log in to WhatsApp Web.")
time.sleep(60)  # Adjust this sleep time according to your needs

# Define the target chat/contact name
target_chat = 'Kaka'

# Search for the chat
search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.click()
search_box.send_keys(target_chat)
search_box.send_keys(Keys.ENTER)

# Wait for the chat to load
time.sleep(5)
wait = WebDriverWait(driver, 10)
# Scroll up to load messages (adjust the range as needed)
for _ in range(5):
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]')))
    element.click()
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME + Keys.CONTROL)
    time.sleep(2)

# Extract messages
# Ensure the XPath is up-to-date with WhatsApp Web's structure
messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//div[contains(@class, "copyable-text")]')

# Define a function to parse order details from a message
def parse_order_details(message):
    order_details = {}
    # Regular expression patterns to match order details
    order_id_pattern = r"Order ID:\s*(\S+)"
    product_pattern = r"Product:\s*(.+)"
    quantity_pattern = r"Quantity:\s*(\d+)"
    price_pattern = r"Price:\s*(\d+)"
    
    # Search for patterns in the message text
    order_id_match = re.search(order_id_pattern, message)
    product_match = re.search(product_pattern, message)
    quantity_match = re.search(quantity_pattern, message)
    price_match = re.search(price_pattern, message)
    
    # Extract matched details and add to the dictionary
    if order_id_match:
        order_details['Order ID'] = order_id_match.group(1)
    if product_match:
        order_details['Product'] = product_match.group(1)
    if quantity_match:
        order_details['Quantity'] = quantity_match.group(1)
    if price_match:
        order_details['Price'] = price_match.group(1)
    
    return order_details

# Parse the extracted messages
orders = []
for message_element in messages:
    message_text = message_element.text
    order_details = parse_order_details(message_text)
    if order_details:
        orders.append(order_details)

# Print the extracted order details
for order in orders:
    print(order)

# Save the extracted order details to a CSV file
csv_file = r'C:\Users\Pratyusha Chatterjee\Documents\order_details1.csv'  # Change this path to your desired location
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Order ID', 'Product', 'Quantity', 'Price'])
    writer.writeheader()
    writer.writerows(orders)

print(f"Order details have been saved to {csv_file}")

# Close the driver
driver.quit()
