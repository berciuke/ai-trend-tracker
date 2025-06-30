import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Pobieranie leksykonu VADER
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')
INPUT_FILE = os.path.join("data", "reddit_posts_processed.csv")
OUTPUT_FILE = os.path.join("data", "reddit_posts_with_sentiment.csv")
VISUALIZATIONS_DIR = "docs"

# Funkcja AI-generated, ładowanie danych z CSV
def load_data(filename):
    if not os.path.exists(filename):
        print(f"Błąd: Plik wejściowy nie został znaleziony w {filename}")
        print("Proszę najpierw uruchomić preprocess.py.")
        return None
    return pd.read_csv(filename)

# Analiza sentymentu tekstu
def analyze_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    # Zastosowanie analizatora VADER
    df['sentiment_scores'] = df['processed_text'].fillna('').apply(lambda text: sia.polarity_scores(text))
    
    # Rozdzielenie wyników na osobne kolumny
    df['compound_score'] = df['sentiment_scores'].apply(lambda score_dict: score_dict['compound'])
    df['positive_score'] = df['sentiment_scores'].apply(lambda score_dict: score_dict['pos'])
    df['negative_score'] = df['sentiment_scores'].apply(lambda score_dict: score_dict['neg'])
    df['neutral_score'] = df['sentiment_scores'].apply(lambda score_dict: score_dict['neu'])
    
    # Klasyfikacja na podstawie wyniku compound
    df['sentiment_label'] = df['compound_score'].apply(lambda c: 'positive' if c >= 0.05 else ('negative' if c <= -0.05 else 'neutral'))

    return df

# Funkcja AI-generated, wykresy i chmura słów
def generate_visualizations(df):
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    # Wykres słupkowy rozkładu sentymentu
    print("Generowanie wykresu rozkładu sentymentu...")
    sentiment_counts = df['sentiment_label'].value_counts()
    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'])
    plt.title('Rozkład Sentymentu Postów Reddit')
    plt.xlabel('Sentyment')
    plt.ylabel('Liczba Postów')
    plt.xticks(rotation=0)
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, 'sentiment_distribution.png'))
    plt.close()

    # Chmura słów
    print("Generowanie chmury słów...")
    text_for_wordcloud = " ".join(df['processed_text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_for_wordcloud)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Najczęściej Występujące Słowa w Postach Reddit')
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, 'wordcloud.png'))
    plt.close()

if __name__ == "__main__":
    print("Rozpoczynanie analizy sentymentu...")
    df = load_data(INPUT_FILE)

    if df is not None:
        df = analyze_sentiment(df)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Pomyślnie przeanalizowano sentyment i zapisano wyniki do {OUTPUT_FILE}")
        
        generate_visualizations(df)
        print(f"Wizualizacje zapisano do katalogu '{VISUALIZATIONS_DIR}'.")
