import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("career_text_dataset.csv")

# Remove empty rows if any
df = df.dropna(subset=["text", "career"])

# Input and output
X = df["text"]
y = df["career"]

# Convert text into numbers
vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_vectorized, y)

# Save model and vectorizer
joblib.dump(model, "career_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")
print("Saved: career_model.pkl and vectorizer.pkl")




