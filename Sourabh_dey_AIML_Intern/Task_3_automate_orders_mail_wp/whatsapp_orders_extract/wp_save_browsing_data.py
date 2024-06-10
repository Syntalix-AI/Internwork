import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys

# Configure Edge service and options
edge_service = Service('msedgedriver.exe')
edge_options = Options()
edge_options.add_argument(r"user-data-dir=C:\Users\Sourabh_Dey\Desktop\automate_orders\whatsapp_orders\wp_data")  # Set the user data directory for saving the whatsapp data
edge_options.add_argument("--start-maximized")
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option('useAutomationExtension', False)

# Launch the Edge browser
browser = webdriver.Edge(service=edge_service, options=edge_options)

# Open WhatsApp Web
browser.get("https://web.whatsapp.com/")

# Wait for the user to scan the QR code and login
print("Please scan the QR code to log in to WhatsApp Web.")
time.sleep(30)  # Adjust sleep time as needed

print("Session data saved.")
browser.quit()
