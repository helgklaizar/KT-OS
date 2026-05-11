import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove special characters but keep punctuation like '!' or '?'
    text = re.sub(r'[^\w\s\!\?]', '', text)
    return text.lower().strip()

def main():
    print("🚀 Starting EDA (Exploratory Data Analysis) on Support Tickets...")
    
    # 1. Load Data
    data_path = 'src/data/raw_tickets.csv'
    df = pd.read_csv(data_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    # 2. Basic Cleaning
    df['ticket_text'] = df['ticket_text'].apply(clean_text)
    
    # 3. Feature Engineering
    # Calculate ticket length
    df['ticket_length'] = df['ticket_text'].apply(len)
    # Count exclamation marks as a proxy for urgency/frustration
    df['exclamation_count'] = df['ticket_text'].apply(lambda x: x.count('!'))
    
    print("\nData Preview (with new features):")
    print(df[['ticket_text', 'department', 'ticket_length', 'exclamation_count']].head())
    
    # 4. Create Visualizations
    os.makedirs("docs/plots", exist_ok=True)
    
    # Plot 1: Distribution of Departments
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='department', order=df['department'].value_counts().index, palette='viridis')
    plt.title("Distribution of Support Tickets by Department")
    plt.xlabel("Number of Tickets")
    plt.ylabel("Department")
    plt.tight_layout()
    plt.savefig("docs/plots/department_distribution.png")
    plt.close()
    
    # Plot 2: Ticket Length by Department
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='department', y='ticket_length', palette='Set2')
    plt.title("Ticket Length vs Department")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("docs/plots/ticket_length_boxplot.png")
    plt.close()
    
    print("\n✅ EDA completed! Plots saved to 'docs/plots/'.")

if __name__ == "__main__":
    main()
