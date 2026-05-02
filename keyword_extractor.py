from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text):
    if not text or len(text.strip()) == 0:
        return []
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20,
        ngram_range=(1, 2)  #captures phrases like "machine learning","oprating system",etc
    )
    try:
        X = vectorizer.fit_transform([text])
        keywords = vectorizer.get_feature_names_out().tolist()
        
        #Remove weak/generic words
        
        blacklist = {
            "experience", "knowledge", "skills",
            "ability", "strong", "good",
            "understanding", "work", "team",
            "systems", "development"
        }

        #Clean keywords
        
        filtered_keywords = [
            word for word in keywords
            if word not in blacklist and len(word) > 2
        ]
        return filtered_keywords
    except Exception as e:
        print("Keyword extraction error:", e)
        return []