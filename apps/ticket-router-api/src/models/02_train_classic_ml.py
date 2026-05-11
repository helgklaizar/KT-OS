import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from catboost import CatBoostClassifier

def main():
    print("🚀 Starting Sprint 2: Classic Machine Learning Pipeline...")
    
    # 1. Load Data
    data_path = 'src/data/raw_tickets.csv'
    df = pd.read_csv(data_path)
    
    # Drop rows with NaN in critical columns
    df = df.dropna(subset=['ticket_text', 'department'])
    
    # We want to predict 'department' from 'ticket_text'
    X = df['ticket_text']
    y = df['department']
    
    # 2. Text Vectorization (TF-IDF)
    print("⏳ Vectorizing text data (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=2000, stop_words='english', ngram_range=(1, 2))
    X_vectorized = vectorizer.fit_transform(X)
    
    # 3. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Data Split -> Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    
    # 4. Train Model (CatBoost)
    # CatBoost is great but can be slow on large sparse matrices, so we use iterations=100 for speed in our lab.
    print("🤖 Training CatBoost Classifier (this might take a few moments)...")
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        loss_function='MultiClass',
        verbose=10,
        random_seed=42
    )
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=10)
    
    # 5. Evaluate
    print("\n📊 Evaluating the model...")
    y_pred = model.predict(X_test)
    
    # CatBoost returns predictions as a 2D array of strings, we flatten it
    y_pred = [pred[0] for pred in y_pred]
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 6. Save the model and vectorizer
    os.makedirs('src/models/saved', exist_ok=True)
    
    # Save vectorizer
    joblib.dump(vectorizer, 'src/models/saved/tfidf_vectorizer.pkl')
    
    # Save CatBoost model
    model.save_model('src/models/saved/catboost_classifier.cbm')
    
    print("💾 Model and Vectorizer saved successfully in 'src/models/saved/'.")

if __name__ == '__main__':
    main()
