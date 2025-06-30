import praw
import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, "..", ".env")
load_dotenv(env_path)

# WAŻNE: Uzupełnij plik .env
CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "PATRZ_PLIK_ENV_EXAMPLE")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "PATRZ_PLIK_ENV_EXAMPLE")
USER_AGENT = "TrendTracker/0.1 by berciuke"

SUBREDDITS = ["technology", "investing", "wallstreetbets"]
# Limity postów dla różnych okresów czasowych - zapewnia zróżnicowany zbiór danych
POST_LIMITS = {
    "year": 1000,
    "month": 500,
    "week": 250,
    "day": 100,
}
TOTAL_POSTS_ESTIMATE = len(SUBREDDITS) * sum(POST_LIMITS.values())

# Tworzenie instancji PRAW do interakcji z API Reddit
def get_reddit_instance():
    if CLIENT_ID == "PATRZ_PLIK_ENV_EXAMPLE" or CLIENT_SECRET == "PATRZ_PLIK_ENV_EXAMPLE":
        print("BŁĄD: Klucze API Reddita nie zostały znalezione w pliku .env.")
        print("Proszę skopiować .env.example do .env i uzupełnić swoimi danymi.")
        return None
    
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )
    return reddit

# Pobieranie postów 
def scrape_subreddits(reddit, subreddits, limits):
    all_posts = []
    seen_posts = set() # eliminacja duplikatów

    for subreddit_name in subreddits:
        print(f"--- Rozpoczynanie pobierania z r/{subreddit_name} ---")
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for period, limit in limits.items():
                print(f"Pobieranie {limit} najlepszych postów z okresu: '{period}'...")
                # Używam .top() z filtrem czasowym dla większej różnorodności danych
                for post in subreddit.top(time_filter=period, limit=limit):
                    if post.id not in seen_posts:
                        all_posts.append({
                            "subreddit": subreddit_name,
                            "title": post.title,
                            "score": post.score,
                            "id": post.id,
                            "url": post.url,
                            "num_comments": post.num_comments,
                            "created_utc": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                            "body": post.selftext,
                        })
                        seen_posts.add(post.id)
                time.sleep(1) # opóźnienie, przez limity API 
        except Exception as e:
            print(f"Nie udało się pobrać danych z r/{subreddit_name}. Powód: {e}")
            continue
            
    return all_posts

# Funkcja AI-generated
def save_to_csv(posts, filename): 
    if not posts:
        print("Brak postów do zapisania.")
        return
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=posts[0].keys())
        writer.writeheader()
        writer.writerows(posts)

if __name__ == "__main__":
    print("Uruchamianie ulepszonego scrapera Reddit...")
    print(f"Szacowana liczba postów do pobrania: {TOTAL_POSTS_ESTIMATE}")
    print(f"Szacowany czas operacji: {round(len(SUBREDDITS) * len(POST_LIMITS) * 1.5 / 60, 1)} minut")
    
    reddit = get_reddit_instance()
    if reddit:
        posts = scrape_subreddits(reddit, SUBREDDITS, POST_LIMITS)
        if posts:
            save_to_csv(posts, "reddit_posts.csv")
            print(f"Pomyślnie pobrano {len(posts)} unikalnych postów i zapisano do data/reddit_posts.csv")
        else:
            print("Nie pobrano żadnych postów. Sprawdź swoje dane uwierzytelniające i nazwy subredditów.")
