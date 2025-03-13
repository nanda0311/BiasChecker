
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset

# Load dataset
df = pd.read_csv("bias_dataset.csv")

# Convert pandas dataframe to Hugging Face Dataset
dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)

# Load Tokenizer
MODEL_NAME = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(examples["Article Text"], truncation=True, padding="max_length", max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Load Model
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Train the model
trainer.train()

# Save the trained model
model.save_pretrained("model")
tokenizer.save_pretrained("model")

print("Training complete! Model saved in 'model/' directory.")
                    