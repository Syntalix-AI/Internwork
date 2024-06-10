import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome()

driver.get("https://web.whatsapp.com")
time.sleep(30)  # Wait for QR code to be scanned and chats to load

def get_unread_messages():
    try:
        # Locate unread chats
        unread_chats = driver.find_elements(By.CSS_SELECTOR, "span[aria-label*='unread message']")
        for chat in unread_chats:
            try:
                chat.click()  # Click on the unread chat
                time.sleep(2)  # Wait for the chat to open
                
                # Try to extract sender information for personal chats
                # This part is not working
                try:
                    sender = driver.find_element(By.CSS_SELECTOR, "header._24-Ff > div._2fq0t > div._3sMZR > span._ahxt.x1ypdohk.xt0b8zv._ao3e").text
                except:
                    # If personal chat sender info not found, extract group chat sender info
                    sender_elements = driver.find_elements(By.CSS_SELECTOR, "span[aria-label*=':']")
                    if sender_elements:
                        sender = sender_elements[0].get_attribute('aria-label').replace(':', '')
                    else:
                        sender = "Unknown"

                # Extract unread messages
                # This part is working, but I am getting all the texts (after the last text I sent) from the person who has sent the unread text
                messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in")
                for message in messages:
                    try:
                        msg_text = message.find_element(By.CSS_SELECTOR, "span.selectable-text").text
                        print(f"Sender: {sender}, Unread message: {msg_text}")
                    except Exception as e:
                        print("Error extracting message text:")
                        traceback.print_exc()
            except Exception as e:
                print("Error opening chat or extracting sender information:")
                traceback.print_exc()
    except Exception as e:
        print("Error locating unread chats:")
        traceback.print_exc()

get_unread_messages()
driver.quit()
