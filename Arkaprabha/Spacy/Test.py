import spacy
from pathlib import Path

# Load the fine-tuned model
output_dir = Path("./fine-tuned-model")
nlp = spacy.load(output_dir)

# Define your custom input text
input_text = "John Doe orders 5 apples, 3 oranges, and 2 bananas to be delivered to 123 Main Street, Cityville"

# Process the input text with the fine-tuned model
doc = nlp(input_text)

# Extract the predicted entities
name = None
address = None
items = None

print("Entities:", doc.ents)
print("Text:", doc.text)
print("Tokens:")
for token in doc:
    print(token.text, token.pos_, token.dep_, token.ent_type_, token.ent_iob_)
for ent in doc.ents:
    if ent.label_ == "NAME":
        name = ent.text
    elif ent.label_ == "ADDRESS":
        address = ent.text
    elif ent.label_ == "ITEMS":
        items = ent.text

# Print the extracted entities
if name:
    print(f"Name: {name}")
if address:
    print(f"Address: {address}")
if items:
    print(f"Items: {items}")
