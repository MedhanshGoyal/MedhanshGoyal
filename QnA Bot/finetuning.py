import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import Dataset

# Step 1: Load JSON data
with open('fine_tuning_data.json', 'r') as f:
    data = json.load(f)

# Step 2: Create a dataset
dataset = Dataset.from_dict(data)

# Step 3: Define the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt-3.5-turbo')
model = AutoModelForSeq2SeqLM.from_pretrained('gpt-3.5-turbo')

# Step 4: Tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['context'] + examples['input'], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Step 5: Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Step 6: Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Step 7: Fine-tune the model
trainer.train()

# Step 8: Save the fine-tuned model
model.save_pretrained('./fine_tuned_qna_model')
tokenizer.save_pretrained('./fine_tuned_qna_model')
