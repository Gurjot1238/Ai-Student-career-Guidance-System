import pandas as pd
import io
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    print("🚀 Booting up the Random Forest NLP Trainer...\n")

    # 1. THE DATASET (Hardcoded so you never have to worry about missing CSVs)
# I copied the ultimate Data Scientist profile 5 times to force the trees to learn it!
    data = """text,career
"predictive modeling with python and r","Data Scientist"
"i love doing stats and building machine learning models","Data Scientist"
"data manipulation using pandas numpy and scikit-learn","Data Scientist"
"math statistics algorithms and heavy python scripting","Data Scientist"
"big data processing spark hadoop machine learning","Data Scientist"
"python machine learning data science pandas numpy statistics deep learning sql","Data Scientist"
"python machine learning data science pandas numpy statistics deep learning sql","Data Scientist"
"python machine learning data science pandas numpy statistics deep learning sql","Data Scientist"
"python machine learning data science pandas numpy statistics deep learning sql","Data Scientist"
"python machine learning data science pandas numpy statistics deep learning sql","Data Scientist"
"training large language models and nlp","AI Engineer"
"computer vision opencv deep learning keras","AI Engineer"
"i build neural networks using tensorflow","AI Engineer"
"creating ai agents chatbots and generative ai using python","AI Engineer"
"optimizing deep learning models for inference","AI Engineer"
"backend software architecture c# .net core","Software Developer"
"writing high performance c++ code and system design","Software Developer"
"i am a programmer who loves solving dsa problems","Software Developer"
"full lifecycle software engineering java spring","Software Developer"
"building scalable microservices backend coder","Software Developer"
"building responsive websites with tailwind and js","Web Developer"
"i am a frontend coder focusing on react and nextjs","Web Developer"
"html css javascript dom manipulation and animations","Web Developer"
"creating web applications typescript nodejs frontend","Web Developer"
"full stack web coding vuejs and express","Web Developer"
"ios development using swift and xcode","App Developer"
"building cross platform apps with react native","App Developer"
"mobile application lifecycle android studio kotlin","App Developer"
"i want to make smartphone apps using flutter","App Developer"
"publishing apps to the app store and play store","App Developer"
"creating dashboards in tableau and powerbi","Data Analyst"
"cleaning messy excel sheets and making pivot tables","Data Analyst"
"sql queries for business intelligence and reporting","Data Analyst"
"i like visualizing data trends using python and matplotlib","Data Analyst"
"finding business insights from large datasets analytics","Data Analyst"
"threat hunting malware analysis and cryptography","Cyber Security Analyst"
"i do bug bounties and penetration testing","Cyber Security Analyst"
"infosec compliance vulnerability scanning","Cyber Security Analyst"
"defending networks against ddos and hackers kali","Cyber Security Analyst"
"incident response security operations center soc","Cyber Security Analyst"
"""

# 2. Read the data and save it as a CSV
    df = pd.read_csv(io.StringIO(data))
    
    # ADD THIS LINE TO SAVE THE FILE:
    df.to_csv("career_dataset.csv", index=False) 
    
    X = df["text"]
    y = df["career"]

    # 3. TEXT VECTORIZATION (NLP Magic)
    print("🔡 Converting skill sentences into math (TF-IDF)...")
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
    X_vectorized = vectorizer.fit_transform(X)

    # 4. TRAIN THE RANDOM FOREST
    print("🌲 Training the Random Forest model... (This will be quick)")
    # n_estimators=150 creates 150 decision trees for high accuracy
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_vectorized, y)

    # 5. SAVE AND EXPORT
    print("\n💾 Saving models to your hard drive...")
    try:
        joblib.dump(model, "career_model_rf.pkl")
        joblib.dump(vectorizer, "vectorizer_rf.pkl")
        
        print("\n" + "="*50)
        print("✅ SUCCESS: Model Trained and Pickled!")
        print("="*50)
        print("You can now find these files in your folder:")
        print(f" 📂 {os.path.abspath('career_model_rf.pkl')}")
        print(f" 📂 {os.path.abspath('vectorizer_rf.pkl')}")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ ERROR SAVING FILES: {str(e)}")

# Run the main function safely
if __name__ == "__main__":
    main()