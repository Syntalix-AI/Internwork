#importing the necessary libraries
import imaplib
import email
import yaml
import time



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
model_for_image = genai.GenerativeModel('gemini-pro-vision')
model_for_text = genai.GenerativeModel('gemini-pro')

# the prompt
prompt1 = """from every string, retrieve the week_day, date, time_of_order, Sender_Name, Sender_Email, nested_list_of_order_with_price,mode_of_payment and pass them in a comma separated format only,
            well if the subject contains hinglish or bengali also, translate them properly, remove those having empty subjects or unrelated to orders of vegetable or fruits,
            separate mail id and sender name and give the headers or column names as - week_day, date, time_of_order, Customer_Name, Contact, Order_with_Quantity,mode_of_payment-
            example -
            Sunday, 9 Jun 2024, 20:02:58, Sourabh Dey, souravdeyuhd@gmail.com, [4kg apple, 3kg onion, 5kg Mangoes], [Credit card, or Debit card] -
            like this, add those brackets like them, ignore the irrelevant ones!
            """

prompt2 = " if subject is related to orders return 'yes' or else return 'no', nothing extra, well if the subject contains hinglish or bengali also, translate them properly "

def Compile_Orders(prompt,data):
    response = model_for_text.generate_content(f'{prompt} for \n{data}')
    orders = response.text
    with open('orders_text_gmail.txt', 'w') as file:
        file.write(orders)
    return orders

#-----------------------------------------

def Check_text(prompt,data):
    response = model_for_text.generate_content(f'{prompt} for \n{data}')
    choice = response.text.strip().lower()
    return choice






def save_to_csv(input_file, output_file):
    # Read the text file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the text to a structured format
    orders = []
    for line in lines[1:]:  # Skip the header line
        parts = line.strip().split(', ', 6)
        if len(parts) == 7:
            order = {
                'week_day': parts[0],
                'date': parts[1],
                'time_of_order': parts[2],
                'Sender_Name': parts[3],
                'Sender_Email': parts[4],
                'Order_with_Quantity': parts[5],
                'mode_of_payment': parts[6]
            }
            orders.append(order)

    # Write the structured data to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['week_day', 'date', 'time_of_order', 'Sender_Name', 'Sender_Email', 'Order_with_Quantity', 'mode_of_payment']
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
        parts = line.strip().split(', ', 6)
        if len(parts) == 7:
            order = {
                'week_day': parts[0],
                'date': parts[1],
                'time_of_order': parts[2],
                'Sender_Name': parts[3],
                'Sender_Email': parts[4],
                'Order_with_Quantity': parts[5],
                'mode_of_payment': parts[6]
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



#connecting to my mail
with open("cred.yaml") as f:
    creds = f.read()

my_cred = yaml.load(creds, Loader = yaml.FullLoader) #will create dictionary out of the contents

#print(my_cred)
mail, pw = my_cred['user'], my_cred['password']

imap_url = 'imap.gmail.com'

#connecting with google with Secure Shell

my_mail = imaplib.IMAP4_SSL(imap_url)

#loggin in
my_mail.login(mail, pw)

#selecting the particular part for fetching the messages
my_mail.select("Inbox")

key = 'FROM'
values = ['souravdeyuhd@gmail.com','deysourabh8981@gmail.com','uhddey@gmail.com'] # parsing through list of emails
#values = ['123@gmail.com','rtitj@gmail.com'] # some invalid emails used here
print("\nEXTRACTING MAILS, PLEASE WAIT........\n")
time.sleep(4)

mail_content = []
for value in values :
    _ , data = my_mail.search(None, key, value)

    #print(type(data))

    mail_id_list = data[0].split() #will give the IDs of the mails which are sent from given mail 

    #print(len(data[0].split()))
    msgs = []

    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 will fetch mails containg ASCII body only
        msgs.append(data)

    #print(msgs)


    #now iterating through each of the messages
    #while True:
    for msg in msgs[::-1]: #starting from the end / reverse
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg = email.message_from_bytes((response_part[1]))
                #print(my_msg)
                #print(type(my_msg))
                subject = my_msg['subject']
                sender = my_msg['from']
                date_and_time = my_msg['date']
                
                print("_____________________________________________\n")
                print("subj:", my_msg['subject'])
                print("from:", my_msg['from'])
                print("date:", my_msg['date'])
                print("body")
                # now parsing through the body=
                for part in my_msg.walk():
                    #print(part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload()
                        #print(type(part.get_payload()))
                        print(part.get_payload())
                        with open("Gmail_contents.txt","a") as gmail_content :
                            gmail_content.write(f"subject: {subject}\nfrom: {sender}\ndate: {date_and_time}\nbody: \n{body}\n-------------------------------\n")
                        mail_content.append({"date_and_time":f'{date_and_time}',"sender":f'{sender}',"Subject":f'{subject}','body':f'{body}'})
            
#print("Saved contents successfully")
print(mail_content)
print("\nRemoving Null and irrevelant Values.....\n")
time.sleep(3)
print("\nGmail Content File has been Created Successfully...\n")
time.sleep(2)
print("\nExtracting Necessary Headers....\n")
Compile_Orders(mail_content,prompt1)

#print(Compile_Orders(prompt1,data))
                        
save_to_pdf('orders_text_gmail.txt', 'orders_gmail_pdf.pdf')
save_to_json('orders_text_gmail.txt', 'orders_gmail_json.json')
save_to_csv('orders_text_gmail.txt', 'orders_gmail_csv.csv')
time.sleep(2)
print("\nCompiled Order__gmail_text.txt, Orders_gmail_pdf.pdf, Orders_gmail_json.json successfully...\n")
print("\nYour Data has been compiled successfully!\nYou Can check it below- ")
                
ch = input("Check the DataFrame?(y/n): ").strip().lower()

if ch == 'y':
    import pandas as pd
    df = pd.read_csv("orders_csv.csv")
    print(df)
    print(df.info())
else:
    exit()






