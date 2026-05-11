import os
import sqlite3
import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_knowledge_base():
    """Generates fake markdown documents for the RAG Vector DB."""
    os.makedirs("src/data/kb", exist_ok=True)
    
    policies = {
        "Refund_Policy": "All refunds must be processed within 14 days of purchase. The item must be in its original packaging. Contact support@company.com for initiation.",
        "Remote_Work_Policy": "Employees are allowed to work remotely 3 days a week. Core hours are 10 AM to 3 PM EST. Security VPN must be active at all times.",
        "Onboarding_Guide": "Welcome! On your first day, please ensure you have access to Jira, Slack, and the internal Git repository. Contact IT at ext 404 for hardware issues.",
        "AI_Usage_Guidelines": "Do not input sensitive customer PII into public LLMs. Use the internal Antigravity proxy for all RAG and AI generations."
    }
    
    for title, content in policies.items():
        with open(f"src/data/kb/{title}.md", "w", encoding="utf-8") as f:
            f.write(f"# {title.replace('_', ' ')}\n\n{content}\n")
    print(f"✅ Generated {len(policies)} Knowledge Base documents in 'src/data/kb/'.")

def generate_sql_db():
    """Generates a fake SQLite database for structured data querying."""
    os.makedirs("src/data/db", exist_ok=True)
    db_path = "src/data/db/company.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Employees Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Populate Employees
    cursor.execute('DELETE FROM employees') # clear if exists
    for _ in range(50):
        name = fake.name()
        dept = random.choice(["Engineering", "Sales", "HR", "Marketing", "Product"])
        email = f"{name.replace(' ', '.').lower()}@company.com"
        cursor.execute('INSERT INTO employees (name, department, email) VALUES (?, ?, ?)', (name, dept, email))
        
    conn.commit()
    conn.close()
    print(f"✅ Generated fake SQLite database at '{db_path}' with 50 employee records.")

def main():
    print("🚀 Generating Fake Data Ecosystem...")
    generate_knowledge_base()
    generate_sql_db()
    print("🎉 Done! Data is ready for RAG and LLM querying.")

if __name__ == "__main__":
    main()
