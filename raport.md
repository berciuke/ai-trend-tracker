Raport Projektowy: Analiza Sentymentu i Dynamiki Trendów na Reddicie

Arkadiusz Pająk,  Czerwiec 2025

---

## 1. Wprowadzenie i Cel Projektu

### 1.1. Geneza i motywacja

Pomysł na ten projekt zrodził się w ramach przedmiotu "Inteligencja Obliczeniowa". Szukałem tematu, który byłby zarówno ciekawy, jak i możliwy do zrealizowania w ramach moich obecnych umiejętności, a jednocześnie pozwoliłby mi zastosować w praktyce wiedzę zdobytą na laboratoriach. Zainspirował mnie temat nr 9 z listy projektów - "Analiza tekstu z mediów społecznościowych".

Reddit jest pełen ludzkich opinii na właściwie każdy temat oraz nietrudno jest pozyskać ("zescrapować") z niego posty. Pomyślałem, że analiza sentymentu w społecznościach technologicznych i inwestycyjnych mogłaby być fascynująca. Czy nowa technologia jest przyjmowana z entuzjazmem? Czy nastroje na forach inwestycyjnych odzwierciedlają wahania na giełdzie? To pytania, na które chciałem spróbować odpowiedzieć, tworząc ten projekt.

### 1.2. Założenia i cele

1. &#x20;Pobranie postów z Reddita przez API (PRAW), samodzielnie ogarniając autoryzację i zapis do CSV.
2. Oczyszczanie, tokenizacja, usuwanie stopwordów, lematyzacja – wszystko zbudowane na bazie kodu pisanego na labach.
3. Użycie prostego, ale skutecznego VADER-a do oceny nastrojów.
4. &#x20;Postawienie lekkiej appki w Streamlicie, która pokazuje wyniki i pozwala je eksplorować.

Zależało mi na tym, żeby kod był maksymalnie prosty i czytelny – tak, żeby ktoś z mojego roku mógł bez problemu przejrzeć i zrozumieć każdy etap. Nie kopiowałem gotowców – świadomie realizowałem projekt, ucząc się po drodze i testując różne podejścia.

### 1.3. Wybrane technologie

- **Python, Pandas, Matplotlib**
- **PRAW (Python Reddit API Wrapper)** Najprostsze narzędzie do scrapowania danych z Reddita.
- **NLTK (Natural Language Toolkit):** Główne narzędzie do przetwarzania języka naturalnego. Korzystałem z niego na laboratoriach, więc chciałem dalej zgłębiać jego możliwości (tokenizacja, stopwords, lematyzacja, VADER).
- **WordCloud:** Do tworzenia wizualizacji - chmura słów
- **Streamlit:** Do stworzenia interaktywnej aplikacji webowej. Pozwala błyskawicznie przekształcić skrypty analityczne w działającą apkę bez konieczności implementacji  frontendu np. przy użyciu Next.js.

## 2. Realizacja Projektu

### 2.1. Krok 1: Zbieranie Danych (`scraper.py`)

Pierwszym wyzwaniem było zdobycie danych. Zdecydowałem się na scraping Reddita, a konkretnie trzech subredditów: `r/technology`, `r/investing` oraz `r/wallstreetbets`. Wybór był celowy – chciałem mieć mieszankę tematów technologicznych i finansowych, w tym jedno forum (`wallstreetbets`) znane z bardzo emocjonalnego języka i zdolności do wpływania na rzeczywiste rynki finansowe (np. głośna sprawa akcji GameStop i AMC). To pozwalało sprawdzić, jak sentyment użytkowników może mieć przełożenie na decyzje inwestycyjne..

Napisałem skrypt `scraper.py`, który za pomocą biblioteki PRAW łączy się z API Reddita i pobiera najgorętsze posty z wybranych subredditów. Skrypt zapisuje kluczowe informacje o postach (tytuł, treść, autor, data, liczba komentarzy) do pliku `reddit_posts.csv`. Musiałem oczywiście założyć własną "aplikację" na moim koncie Reddit, żeby uzyskać klucze API.&#x20;

### 2.2. Krok 2: Przetwarzanie Wstępne Tekstu (`preprocess.py`)

Surowe dane tekstowe są pełne "śmieci", które mogą zakłócić analizę. Dlatego kolejnym krokiem było ich oczyszczenie. Skrypt `preprocess.py` jest tzw. potokiem przetwarzania, który dla każdego posta wykonuje następujące operacje:

Najpierw wszystko sprowadzałem do małych liter, żeby nie mieć problemów z wielkością znaków.
Potem usuwałem śmieci typu linki, cyfry i znaki specjalne, bo tylko zaśmiecają analizę.
Następnie dzieliłem teksty na pojedyncze słowa (tokeny), żeby dało się na nich pracować.
Z tych słów pozbywałem się tzw. stopwordów, czyli takich „the”, „a”, „is” – słów, które nic nie wnoszą.
Na końcu robiłem lematyzację, czyli sprowadzałem słowa do ich podstawowej formy – dzięki temu „runs”, „running” i „ran” były traktowane jako jedno i to samo.

Cały proces był inspirowany zadaniami z laboratorium. Po przetworzeniu, czyste dane są zapistwane do nowego pliku `reddit_posts_processed.csv`, gotowe do dalszej analizy.

### 2.3. Krok 3: Analiza Sentymentu (`sentiment_analysis.py`)

To serce całego projektu. Do analizy sentymentu użyłem narzędzia **VADER (Valence Aware Dictionary and sEntiment Reasoner)**, które jest częścią biblioteki NLTK. Wybrałem VADERa, ponieważ jest on specjalnie dostosowany do analizy tekstów z mediów społecznościowych – dobrze radzi sobie ze slangiem, emotikonami i wielkimi literami. Jest to model oparty na regułach i słowniku, co czyni go prostym w użyciu i interpretacji, idealnym na potrzeby tego projektu.

Skrypt `sentiment_analysis.py` wczytuje przetworzone dane, a następnie dla każdego posta oblicza cztery wskaźniki VADER:

- `positive`, `negative`, `neutral`: udział słów pozytywnych, negatywnych i neutralnych.
- `compound`: zagregowany wynik od -1 (skrajnie negatywny) do +1 (skrajnie pozytywny).

Na podstawie wyniku `compound` stworzyłem prostą klasyfikację, oznaczając każdy post jako "pozytywny", "neutralny" lub "negatywny". Wyniki wraz z etykietami zapisałem do pliku `reddit_posts_with_sentiment.csv`.

Dodatkowo, w tym skrypcie zaimplementowałem generowanie dwóch kluczowych wizualizacji: wykresu słupkowego pokazującego ogólny rozkład sentymentu oraz chmury słów, która w graficzny sposób pokazuje najczęściej występujące terminy.

## 3. Prezentacja Wyników

### 3.1. Aplikacja Webowa (`app.py`)

Samo przetworzenie danych to nie wszystko – trzeba je jeszcze w przystępny sposób zaprezentować. Do tego celu stworzyłem prostą aplikację webową za pomocą biblioteki Streamlit.

Aplikacja `app.py` pozwala na:

- **Przeglądanie ogólnych wyników:** Na stronie głównej wyświetlają się wizualizacje (rozkład sentymentu i chmura słów) dla całego zbioru danych.
- **Interaktywną analizę:** Użytkownik (w tym przypadku prowadzący) może filtrować wyniki według konkretnego subreddita, aby porównać nastroje panujące w różnych społecznościach.
- **Podgląd danych:** Aplikacja wyświetla również tabelę z przetworzonymi danymi i wynikami sentymentu, co pozwala na bardziej szczegółową inspekcję.

Starałem się, aby interfejs był czysty, prosty i zawierał moje "studenckie" komentarze, tłumaczące co widać w danej sekcji.

## Rozdział 4: Podsumowanie i Wnioski

### 4.1. Wnioski z projektu

Realizacja tego projektu była niezwykle pouczającym doświadczeniem. Udało mi się z powodzeniem przejść przez wszystkie etapy projektu analitycznego – od surowych danych po interaktywną wizualizację. Zrozumiałem, jak ważne jest staranne przygotowanie danych i jak duży wpływ ma ono na końcowe wyniki. Dowiedziałem się też, że nawet proste modele, takie jak VADER, mogą dać ciekawe i wartościowe wyniki, jeśli zostaną poprawnie zastosowane.

Największym wyzwaniem było dla mnie samo zebranie i oczyszczenie danych – to faktycznie, jak mówią specjaliści, zajmuje najwięcej czasu. Ciekawym doświadczeniem było też "ubranie" moich analiz w aplikację Streamlit, co sprawiło, że projekt stał się znacznie bardziej namacalny - taką miałem wizję ;-).

### 4.2 Wnioski z pozyskanych danych

Analiza danych pokazała ciekawe różnice między subredditami. `r/investing` to najbardziej optymistyczna przestrzeń — aż 82% postów miało pozytywny wydźwięk. Można wnioskować, że społeczność ta skupia się na długoterminowych strategiach i dzieleniu się sukcesami, a nie na emocjonalnym reagowaniu na krótkoterminowe wydarzenia.

W `r/technology` natomiast proporcje są mocno zbalansowane – dużo treści neutralnych, sporo pozytywnych i negatywnych. To raczej forum zorientowane na wymianę informacji i nowinki techniczne niż emocjonalne komentarze.

`r/wallstreetbets` zgodnie z oczekiwaniami prezentuje wyraźną przewagę postów pozytywnych, ale też zauważalną obecność negatywnych — co pasuje do jego reputacji jako miejsca, gdzie dominuje hype, ale też dramaty i frustracje po dużych stratach. Ogólny obraz sentymentu pokrywa się więc dobrze z charakterem tych społeczności i potwierdza, że VADER całkiem trafnie je rozróżnia.

### 4.3. Możliwości rozwoju

Oczywiście, ten projekt to dopiero początek. Gdybym miał więcej czasu, mogłbym go rozwinąć o:

- **Analizę w czasie:** Dodać wykresy pokazujące, jak sentyment dla danego tematu (np. konkretnej spółki giełdowej) zmieniał się w czasie.
- **Bardziej zaawansowane modele:** Spróbować użyć modeli opartych na uczeniu maszynowym lub nawet gotowych modeli transformerowych (np. z Hugging Face) i porównać ich wyniki z VADERem.
- **Topic Modelling:** Zastosować algorytmy takie jak LDA, aby automatycznie odkrywać główne tematy dyskusji w zebranych postach.

### 4.4. Zakończenie

Jestem bardzo zadowolony z tego projektu. Dał mi on ogromną satysfakcję i poczucie, że potrafię wykorzystać wiedzę z zajęć do stworzenia czegoś od zera. To zupełnie inne uczucie niż tylko rozwiązywanie pojedynczych zadań na laboratoriach. Widę teraz znacznie lepiej, jak poszczególne elementy – programowanie, statystyka, przetwarzanie języka – łączą się w jedną, spójną całość. Myślę, że to doświadczenie będzie solidnym fundamentem pod dalszą naukę i przyszłe, bardziej zaawansowane projekty.

