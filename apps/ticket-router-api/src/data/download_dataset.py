import os
import pandas as pd
from datasets import load_dataset

def main():
    print("Downloading Customer Support Dataset from HuggingFace...")
    # Using a popular customer support intent dataset from HuggingFace
    # Bitext's customer support dataset is great for classification and intents.
    dataset = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset", split="train")
    
    # Convert to pandas DataFrame
    df = dataset.to_pandas()
    
    # We will sample 5000 rows to keep it manageable for our EDA and training.
    # We will keep 'instruction' (as the ticket text), 'intent', and 'category'
    df = df.sample(n=5000, random_state=42).reset_index(drop=True)
    
    # Rename columns to fit our narrative
    df = df.rename(columns={
        "instruction": "ticket_text",
        "intent": "issue_type",
        "category": "department"
    })
    
    # Select only the columns we need
    df = df[["ticket_text", "issue_type", "department"]]
    
    # Ensure data directory exists
    os.makedirs("src/data", exist_ok=True)
    
    output_path = "src/data/raw_tickets.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset downloaded and saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(df.head())

if __name__ == "__main__":
    main()
