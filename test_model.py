import joblib

# Load saved files
model = joblib.load("career_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Test input
user_text = input("Enter skills/interests: ")

# Convert text
text_vector = vectorizer.transform([user_text])

# Predict
prediction = model.predict(text_vector)[0]

# Probabilities
probabilities = model.predict_proba(text_vector)[0]
classes = model.classes_

# Top 3 predictions
top_indices = probabilities.argsort()[-3:][::-1]

print("\nRecommended Career:", prediction)
print("\nTop 3 Matches:")
for i in top_indices:
    print(f"{classes[i]} - {probabilities[i]*100:.2f}%")
