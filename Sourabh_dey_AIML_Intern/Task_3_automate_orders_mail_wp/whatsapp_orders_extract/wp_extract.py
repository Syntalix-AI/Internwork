import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# -----------------------------
# for text fetching
#for gemini
import google.generativeai as genai
from dotenv import load_dotenv
import os


#importing libraries for format saving data
import csv
from fpdf import FPDF
import json


#loading the model and Load environment variables
load_dotenv()
# Configure the Google API
GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
# Initializing the model
#model_for_image = genai.GenerativeModel('gemini-pro-vision')
model_for_text = genai.GenerativeModel('gemini-pro')

# the prompt
prompt1 = """from every string ignore things like
            (- "<selenium.webdriver.remote.webelement.WebElement
            (session="eba5d1b615ac950386ff5e49ece415bb", element="f.2238420DA8493CFB3C49703AA9E7348E.d.A0E51D12E552A9091258BAC0ECB03771.e.37")>]", "'21/12/2022\nMessages are end-to-end encrypted."
        , No one outside of this chat, not even WhatsApp, can read or listen to them. Click to learn more\nTODAY\nYour security code with +91 74349 12344 changed.
            Click to learn more\nYour security code with +91 74349 12344 changed., \nEdited21:01\n "!-)

            and ONLY retrieve the Date,Sender_Name, Contact, nested_list_of_order_with_price,mode_of_payment and pass them in a comma separated format only,
            well if the subject contains hinglish or bengali also, translate them properly, remove those having empty subjects or unrelated to orders of vegetable or fruits,
            separate mail id and sender name and give the headers or column names as - date, Customer_Name,Contact, Order_with_Quantity ,mode_of_payment-
            example -
            9 Jun 2024, Sourabh Dey, 9435678549 or email@gmail.com, [4kg apple, 3kg onion, 5kg Mangoes] , [Credit card, or Debit card] -
            
            like this, add those brackets like them, leave them empty if not found.
            """
prompt2 = """ From the given list, extarct all the orders together and then extract the quanity with name and the mode of payment if any and also with example -
                  Sunday, 9 Jun 2024, 20:02:58, Sourabh Dey, [4kg apple, 3kg onion, 5kg Mangoes], [Credit card, or Debit card] - with the column names as -
                  week_day, date, time_of_order, Customer_Name, Order_with_Quantity,mode_of_payment -
                  leave if any one of them is empty or not there, remeber to separate them using COMMAS not anything else"""

def Compile_Orders(prompt,data):
    response = model_for_text.generate_content(f'{prompt} for \n{data}')
    orders = response.text
    with open('orders_text_whatsapp.txt', 'w') as file:
        file.write(orders)
    return orders

#-----------------------------------------

def Check_text(prompt,data):
    response = model_for_text.generate_content(f'{prompt} for \n{data}')    
    choice = response.text.strip().lower()
    return choice


# -----------------------------------------
# for saving in txt, pdf and json

def save_to_csv(input_file, output_file):
    # Read the text file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the text to a structured format
    orders = []
    for line in lines[1:]:  # Skip the header line
        parts = line.strip().split(', ', 4)
        if len(parts) == 5:
            order = {
                #'week_day': parts[0],
                'date': parts[0],
                #'time_of_order': parts[2],
                'Sender_Name': parts[1],
                'Contact': parts[2],
                'Order_with_Quantity': parts[3],
                'mode_of_payment': parts[4]
            }
            orders.append(order)

    # Write the structured data to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['date', 'Sender_Name', 'Contact', 'Order_with_Quantity', 'mode_of_payment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for order in orders:
            writer.writerow(order)

def save_to_json(input_file, output_file):
    # Read the text file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the text to a structured format
    orders = []
    for line in lines[1:]:  # Skip the header line
        parts = line.strip().split(', ', 4)
        if len(parts) == 5:
            order = {
                #'week_day': parts[0],
                'date': parts[0],
                #'time_of_order': parts[2],
                'Sender_Name': parts[1],
                'Sender_Contact': parts[2],
                'Order_with_Quantity': parts[3],
                'mode_of_payment': parts[4]
            }
            orders.append(order)

    # Write the structured data to a JSON file
    with open(output_file, 'w') as jsonfile:
        json.dump(orders, jsonfile, indent=4)

        
def save_to_pdf(input_file, output_file):
    # Read the text file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Create a PDF instance
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Write each line to the PDF
    for line in lines:
        pdf.cell(200, 10, txt=line.strip(), ln=True)

    # Save the PDF
    pdf.output(output_file)





# ----------------------------------------
# Configure Edge service and options
edge_service = Service('msedgedriver.exe')
edge_options = Options()
edge_options.add_argument(r"user-data-dir=C:\Users\Sourabh_Dey\Desktop\automate_orders\whatsapp_orders\wp_data")  # Set the user data directory
edge_options.add_argument("--start-maximized")
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option('useAutomationExtension', False)

# Launch the Edge browser
browser = webdriver.Edge(service=edge_service, options=edge_options)

# Open WhatsApp Web
browser.get("https://web.whatsapp.com/")

# Wait for WhatsApp Web to load
WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
)

# Navigate to the specific chat or group
customers = ["Maa"]# Replace with the actual chat or group name

print("\nEXTRACTING AND PARSING CHATS, PLEASE WAIT........\n")

orders = []

for chat_name in customers:
    # Locate and clear the search box
    search_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
    )
    search_box.clear()
    time.sleep(2)
    search_box.click()
    #search_box.clear()  # Clear the search box
    search_box.send_keys(chat_name)
    time.sleep(5)  # Wait for search results to appear

    chat = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//span[@title='{chat_name}']"))
    )
    chat.click()
    #search_box.clear()

    # Extract messages
    messages = WebDriverWait(browser, 40).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='main']/div[3]/div/div[2]/div[3]"))
    )

    print(type(messages))
    print(messages)
    # Parse and store orders
    for message in messages:
        text = message.text
        orders.append(text)
        

    print(orders)
    

Compile_Orders(prompt1,orders)
print("\nOrders saved to orders_text_whatsapp.txt\n")

print("\nRemoving Null and irrevelant Values.....\n")
time.sleep(3)

save_to_pdf('orders_text_whatsapp.txt', 'orders_pdf_whatsapp.pdf')
save_to_json('orders_text_whatsapp.txt', 'orders_json_whatsapp.json')
save_to_csv('orders_text_whatsapp.txt', 'orders_csv_whatsapp.csv')
time.sleep(2)
print("\nCompiled Order_text_whatsapp.txt, Orders_pdf_whatsapp.pdf, Orders_json_whatsapp.json successfully,orders_csv_whatsapp.csv...\n")
print("\nYour Data has been compiled successfully!\nYou Can check it below- ")
                


browser.quit()

ch = input("Check the DataFrame?(y/n): ").strip().lower()

if ch == 'y':
    import pandas as pd
    df = pd.read_csv("orders_csv_whatsapp.csv")
    print(df)
    print(df.info())
else:
    exit()




# NECESSARY XPATH FOR CHAT DATA FILTERING 

#  //*[@id="main"]/div[3]/div/div[2]/div[3]/div[9]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span


#  //*[@id="main"]/div[3]/div/div[2]/div[3]/div[4]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span

#  //*[@id="main"]/div[3]/div/div[2]/div[3]/div[10]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span



#  //*[@id="main"]/div[3]/div/div[2]/div[3]


#  //*[@id="main"]/div[3]/div/div[2]/div[3]

#  //*[@id="main"]/div[3]/div/div[2]/div[3]/div[4]/div/div/div[1]/div[1]/div[1]/div

#  //*[@id="main"]/div[3]/div/div[2]/div[3]/div[6]/div/div/div/div[1]/div[1]/span/span





