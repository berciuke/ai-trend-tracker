import streamlit as st
import pandas as pd
import os
from PIL import Image

# Konfiguracja ścieżek
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
DATA_FILE = os.path.join(project_root, "data", "reddit_posts_with_sentiment.csv")
VISUALIZATIONS_DIR = os.path.join(project_root, "docs")

st.set_page_config(page_title="AI Trend Tracker", layout="wide")

# Funkcja AI-generated, do ładowania danych z pliku CSV
def load_data(filename):
    if not os.path.exists(filename):
        st.error(f"Plik danych nie został znaleziony w {filename}. Proszę najpierw uruchomić pełny pipeline (scraper, preprocess, sentiment_analysis).")
        return None
    return pd.read_csv(filename)

def main():
    st.title("Analiza Sentymentu i Dynamiki Trendów na Reddicie")
    st.markdown("""
    **Autor:** Arkadiusz Pająk
    **Projekt na przedmiot:** Inteligencja Obliczeniowa

    --- 

    Cześć! To jest moja aplikacja do analizy sentymentu na Reddicie. 
    Zgodnie z założeniami projektu, skupiłem się na stworzeniu prostego, ale funkcjonalnego narzędzia, 
    które pokazuje, jak można analizować nastroje w społecznościach internetowych. 
    Poniżej znajdują się wyniki mojej analizy.
    """)

    df = load_data(DATA_FILE)

    if df is not None:
        st.header("Ogólna Analiza Sentymentu")
        st.markdown("Tutaj możemy zobaczyć ogólny rozkład sentymentu we wszystkich zebranych postach oraz chmurę najczęściej występujących słów.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Rozkład Sentymentu")
            sentiment_dist_path = os.path.join(VISUALIZATIONS_DIR, 'sentiment_distribution.png')
            if os.path.exists(sentiment_dist_path):
                image = Image.open(sentiment_dist_path)
                st.image(image, caption='Rozkład postów na pozytywne, neutralne i negatywne.')
            else:
                st.warning("Wykres rozkładu sentymentu nie został znaleziony. Uruchom `sentiment_analysis.py`.")

        with col2:
            st.subheader("Chmura Słów")
            wordcloud_path = os.path.join(VISUALIZATIONS_DIR, 'wordcloud.png')
            if os.path.exists(wordcloud_path):
                image = Image.open(wordcloud_path)
                st.image(image, caption='Najczęściej występujące słowa w postach.')
            else:
                st.warning("Chmura słów nie została znaleziona. Uruchom `sentiment_analysis.py`.")

        st.header("Szczegółowa Analiza wg Subreddita")
        st.markdown("W tej sekcji można przefiltrować dane, aby zobaczyć analizę dla konkretnego subreddita. To pozwala na porównanie nastrojów w różnych społecznościach.")
        subreddit_options = ['Wszystkie'] + list(df['subreddit'].unique())
        selected_subreddit = st.selectbox("Wybierz Subreddit:", subreddit_options)

        if selected_subreddit == 'Wszystkie':
            filtered_df = df
        else:
            filtered_df = df[df['subreddit'] == selected_subreddit]

        st.subheader(f"Dane dla subreddita: {selected_subreddit}")

        st.write("**Liczba postów wg sentymentu:**")
        st.write(filtered_df['sentiment_label'].value_counts())

        st.write("**Top 5 najbardziej pozytywnych postów:**")
        st.dataframe(filtered_df.nlargest(5, 'compound_score')[['title', 'compound_score']])

        st.write("**Top 5 najbardziej negatywnych postów:**")
        st.dataframe(filtered_df.nsmallest(5, 'compound_score')[['title', 'compound_score']])


        st.header("Surowe Dane")
        st.markdown("Poniżej znajduje się tabela z przetworzonymi danymi, użytymi do analizy. Można ją posortować, klikając na nagłówki kolumn.")
        st.dataframe(filtered_df[[ 'subreddit','title', 'processed_text', 'compound_score', 'sentiment_label']])

if __name__ == "__main__":
    main()
