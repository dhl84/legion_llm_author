import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_text(text):
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    return [token for token in tokens if token not in stop_words]

def get_genre(text):
    sci_fi_keywords = ['future', 'technology', 'space', 'alien', 'robot', 'superpower']
    if any(keyword in text.lower() for keyword in sci_fi_keywords):
        return 'science_fiction'
    return 'other'

def get_themes(text):
    theme_keywords = {
        'power_dynamics': ['power', 'control', 'dominate', 'submission'],
        'gender_roles': ['man', 'woman', 'male', 'female', 'masculine', 'feminine'],
        'transformation': ['change', 'transform', 'metamorphosis'],
        'identity': ['identity', 'self', 'personality'],
    }
    
    themes = []
    for theme, keywords in theme_keywords.items():
        if any(keyword in text.lower() for keyword in keywords):
            themes.append(theme)
    
    return themes

def get_character_types(text):
    character_types = []
    if any(word in text.lower() for word in ['superhuman', 'superpower', 'supernatural']):
        character_types.append('superhuman')
    if 'witch' in text.lower():
        character_types.append('witch')
    return character_types

def get_setting(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    if locations:
        return 'urban' if any(city in locations for city in ['New York', 'Los Angeles', 'Chicago']) else 'rural'
    return 'unknown'

def get_narrative_style(text):
    first_person_pronouns = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    if any(pronoun in text.lower().split() for pronoun in first_person_pronouns):
        return 'first_person'
    return 'third_person'

def get_tone(text):
    positive_words = ['happy', 'joy', 'love', 'excited']
    negative_words = ['sad', 'angry', 'fear', 'dark']
    
    pos_count = sum(1 for word in text.lower().split() if word in positive_words)
    neg_count = sum(1 for word in text.lower().split() if word in negative_words)
    
    if pos_count > neg_count:
        return 'positive'
    elif neg_count > pos_count:
        return 'negative'
    else:
        return 'neutral'

def get_length_category(text):
    word_count = len(text.split())
    if word_count < 1000:
        return 'short'
    elif word_count < 10000:
        return 'medium'
    else:
        return 'long'

def analyze_file(file_path):
    text = load_text(file_path)
    preprocessed_text = ' '.join(preprocess_text(text))
    
    return {
        'filename': os.path.basename(file_path),
        'genre': get_genre(text),
        'themes': get_themes(text),
        'character_types': get_character_types(text),
        'setting': get_setting(text),
        'narrative_style': get_narrative_style(text),
        'tone': get_tone(text),
        'length': get_length_category(text),
        'text': preprocessed_text
    }

def process_folder(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            results.append(analyze_file(file_path))
    return pd.DataFrame(results)

# Example usage
folder_path = '/path/to/your/folder'  # Replace with your folder path
df = process_folder(folder_path)
print(df.head())

# Save results to CSV
df.to_csv('analyzed_texts.csv', index=False)