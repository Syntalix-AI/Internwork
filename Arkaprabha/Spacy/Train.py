import random
import spacy
from spacy.tokens import Span
from spacy.training import Example, offsets_to_biluo_tags
from pathlib import Path
from spacy.util import minibatch

# Load the pre-trained model
nlp = spacy.load("en_core_web_md")

# Convert data to spaCy format
train_data = []
with Path("Train_Data.csv").open(encoding="utf-8") as f:
    next(f)  # Skip the header line
    for line in f:
        parts = line.strip().split(",")
        input_text = ",".join(parts[:-1])
        output_text = parts[-1]

        doc = nlp.make_doc(input_text)
        ents = []

        # Extract name entity
        name_start = output_text.find("Name:")
        name_end = output_text.find("Items:")
        if name_start != -1 and name_end != -1:
            name = output_text[name_start+5:name_end].strip()
            ents.append((name, "NAME"))

        # Extract address entity
        address_start = output_text.find("Address:")
        if address_start != -1:
            address_end = address_start + output_text[address_start:].find("\n")
            address = output_text[address_start+9:address_end].strip()
            ents.append((address, "ADDRESS"))

        # Extract items entity
        items_start = output_text.find("Items:")
        if items_start != -1:
            items = output_text[items_start+6:].split()[:-1]
            items_text = " ".join(items)
            ents.append((items_text, "ITEMS"))

        biluo = offsets_to_biluo_tags(doc, [ent[0] for ent in ents])
        train_data.append((input_text, {"entities": biluo}))

# Create the training data iterator
train_data_iter = list(minibatch(train_data, size=30))

# Configure and start training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for itn in range(15):
        losses = {}
        random.shuffle(train_data_iter)
        batches = train_data_iter
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], sgd=optimizer, losses=losses)
        print(f"Iteration {itn + 1}, Loss: {losses['ner']}")

# Save the fine-tuned model
output_dir = Path("./fine-tuned-model")
if not output_dir.exists():
    output_dir.mkdir()
nlp.to_disk(output_dir)
print("Fine-tuned model saved to", output_dir)
