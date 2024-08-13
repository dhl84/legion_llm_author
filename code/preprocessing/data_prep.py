import os
import pandas as pd
from cleantext import clean
from sklearn.model_selection import train_test_split

def load_and_clean_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    cleaned_text = clean(text,
        fix_unicode=True,
        to_ascii=True,
        lower=True,
        no_line_breaks=True,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=True,
        no_digits=True,
        no_currency_symbols=True,
        no_punct=True,
        replace_with_punct="",
        replace_with_url="",
        replace_with_email="",
        replace_with_phone_number="",
        replace_with_number="",
        replace_with_digit="",
        replace_with_currency_symbol="",
    )
    
    return cleaned_text

def get_labels(filename):
    # This function would need to be implemented based on how you want to assign labels
    # For now, we'll use placeholder values
    return {
        'genre': 'science_fiction',
        'theme': ['power_dynamics', 'gender_roles', 'transformation', 'control'],
        'character_type': 'superhuman',
        'setting': 'contemporary',
        'narrative_style': 'third_person',
        'tone': 'dark',
        'length': 'long_form'
    }

def prepare_dataset(texts, filenames):
    data = []
    for text, filename in zip(texts, filenames):
        labels = get_labels(filename)
        data.append({
            'filename': filename,
            'text': text,
            **labels
        })
    
    df = pd.DataFrame(data)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    return train_df, test_df

def process_folder(folder_path):
    texts = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            cleaned_text = load_and_clean_data(file_path)
            texts.append(cleaned_text)
            filenames.append(filename)
    
    return texts, filenames

# Example usage
folder_path = '/path/to/your/folder'  # Replace with your folder path
cleaned_texts, filenames = process_folder(folder_path)
train_data, test_data = prepare_dataset(cleaned_texts, filenames)

print(f"Training data shape: {train_data.shape}")
print(f"Testing data shape: {test_data.shape}")
print(f"Sample of processed data:")
print(train_data.head())