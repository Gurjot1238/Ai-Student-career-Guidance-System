import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# load dataset
df = pd.read_csv("career_text_dataset.csv")

# convert text to 0/1 matrix
vectorizer = CountVectorizer(binary=True)

X = vectorizer.fit_transform(df["text"])

# convert to array
X_array = X.toarray()

# create final dataset
final_df = pd.DataFrame(X_array)

# add label column
final_df["career"] = df["career"]

# save new dataset
final_df.to_csv("encoded_dataset.csv", index=False)

print("Done!")