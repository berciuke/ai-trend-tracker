import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import re

# Pobieranie pakietów NLTK
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
INPUT_FILE = os.path.join(project_root, "data", "reddit_posts.csv")
OUTPUT_FILE = os.path.join(project_root, "data", "reddit_posts_processed.csv")

# Funkcja AI-generated, do ładowania danych z pliku CSV
def load_data(filename):
    if not os.path.exists(filename):
        print(f"Błąd: Plik wejściowy nie został znaleziony w {filename}")
        print("Proszę najpierw uruchomić scraper.py.")
        return None
    return pd.read_csv(filename)

def preprocess_text(text):
    # Czyszczenie i przetwarzanie tekstu
    if not isinstance(text, str):
        return ""

    # Małe litery, usuwanie URL, znaków specjalnych, cyfr
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # Tokenizacja
    tokens = word_tokenize(text)

    # Usunięcie słów stopowych
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Lematyzacja
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return " ".join(lemmatized_tokens)

if __name__ == "__main__":
    print("Rozpoczynanie przetwarzania wstępnego tekstu...")
    df = load_data(INPUT_FILE)

    if df is not None:
        # Łączenie tytułu i treści w jedną kolumnę
        df['text_to_process'] = df['title'].fillna('') + ' ' + df['body'].fillna('')

        print("Przetwarzanie danych tekstowych... To może potrwać chwilę.")
        df["processed_text"] = df["text_to_process"].apply(preprocess_text)

        # Usunięcie tymczasowej kolumny
        df = df.drop(columns=['text_to_process'])

        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Pomyślnie przetworzono dane i zapisano do {OUTPUT_FILE}")
