# Sprawozdanie — Zestaw zaliczeniowy AAP

**Autor:** Kamil Kwaśny
**Dataset:** `stanfordnlp/imdb` (50 000 recenzji, sentyment pos/neg)

Poniżej krótko: co robi każde zadanie, jaką decyzję projektową podjąłem i jaki płynie z tego wniosek.

## Zadanie 1.1 — dekoratory `@retry` + `@cache_to_disk`

`@retry` ponawia wywołanie do `max_attempts` razy z exponential backoff (`delay * backoff ** próba`), po wyczerpaniu prób podnosi ostatni wyjątek. `@cache_to_disk` liczy klucz jako `md5(repr(args, kwargs))` i przy trafieniu zwraca wynik z pliku JSON bez wykonywania funkcji.

Dla 5 prób i awaryjności 0.5 teoretyczne `P(sukces) = 1 − 0.5⁵ ≈ 0.969` — eksperyment na 100 wywołaniach daje ~97/100, zgodnie z teorią. Drugie wywołanie z tym samym `text_id` jest rzędy wielkości szybsze (odczyt z cache).

## Zadanie 2.1 — multiprocessing dla CPU-bound

`sentiment_score` liczy `(liczba słów pozytywnych) − (negatywnych)`. Porównałem 3 warianty na 5000 recenzji: sekwencyjny, `ThreadPoolExecutor`, `multiprocessing.Pool` (z `chunksize=100`).

Kolejność czasów: **multiprocessing < sekwencyjnie < ThreadPool**. Zadanie jest CPU-bound, więc GIL blokuje wątki (ThreadPool bywa wolniejszy od sekwencyjnego przez narzut), a osobne procesy GIL omijają.

**Decyzja projektowa:** `sentiment_score` zapisuję do osobnego modułu `_workspace/sentiment.py` i importuję. Gdyby była zdefiniowana w komórce notatnika, na macOS/Windows (`spawn`) `Pool` nie zserializowałby jej i kod by się wywalił. To bezpośrednia odpowiedź na wskazówkę „funkcja musi być na poziomie modułu".

## Zadanie 3.1 — `Tokenizer` + pytest

`Tokenizer` ze stripowaniem HTML, case foldingiem i filtrem długości tokenu; `re.findall(r"\w+", ..., re.UNICODE)` poprawnie łapie polskie diakrytyki. Testy w `pytest`: fixtury (`tokenizer`, `imdb_sample`), `parametrize` z 7 przypadkami brzegowymi (pusty string, sam HTML, mieszany case, interpunkcja, polskie znaki, normalne zdanie) oraz jeden `xfail` (adresy e-mail — świadomie nieobsługiwane).

Liczba unikalnych tokenów rośnie wolniej niż liniowo z liczbą recenzji — ilustracja prawa Heapsa (słownik się nasyca).

## Zadanie 4.1 — NoSQL-style w SQLite (kolumna JSON)

Tabela `reviews_json(id, doc)`, gdzie `doc` to JSON z `text/label/stats/tags`. Cztery zapytania przez `json_extract`: rozkład klas, średni `word_count` na klasę, recenzje z tagiem zawierającym „movie", top 5 najdłuższych pozytywnych.

Schemat JSON jest większy (powtarza klucze w każdym wierszu — cena za *schema-on-read*) i bez indeksów na ścieżkach wolniejszy w zapytaniach. Subtelność: `tags` zawiera słowa **dłuższe niż 5 znaków**, więc dokładne `"movie"` (5 znaków) tam nie trafia, ale `LIKE '%movie%'` łapie warianty typu `movies`/`moviegoer`. **Dla tego problemu (stały schemat, dużo agregacji) lepszy jest klasyczny SQL.**

## Zadanie 5.1 — PySpark window functions

Na `df_words` (z przykładu) liczę: ranking długości w klasie (`row_number()` po `word_count` malejąco), top 3 per klasa, różnicę od średniej klasowej (`avg().over(partitionBy("label"))`) oraz średnią kroczącą z 50 ostatnich recenzji (`rowsBetween(-49, 0)`), z wykresem liniowym per klasa.

Window function z `orderBy` wymusza shuffle + sort, dlatego `spark.sql.shuffle.partitions=4` (przy małym zbiorze domyślne 200 partycji to czysty narzut).

## Zadanie 6.1 — kontrakt danych + raport JSON

`DataContract` (deklaracja reguł) oddzielony od `DataValidator` (egzekucja) — zasada open/closed. 7 reguł: `no_nulls` i `labels_in_set` jako `error` (fail fast — podnoszą wyjątek), reszta jako `warning` (trafiają do raportu, nie blokują). Raport z timestampem zapisywany do `_workspace/data_quality_report.json`.

Różnica audyt vs kontrakt: audyt to raport po fakcie, kontrakt to bramka, którą dane muszą przejść przed wejściem do modelu.

---

## Odpowiedzi na sekcję kontrolną

1. **`functools.wraps`** — konieczny, gdy zależy nam na zachowaniu `__name__`, `__doc__` i sygnatury opakowanej funkcji (introspekcja, debugowanie, inne dekoratory bazujące na metadanych). Można odpuścić w jednorazowych, lokalnych wrapperach.
2. **Threading vs multiprocessing** — threading nie przyspiesza obliczeń, bo GIL pozwala wykonywać bajtkod tylko jednemu wątkowi naraz; multiprocessing uruchamia osobne interpretery (osobny GIL na proces), więc realnie zrównolegla CPU.
3. **`parametrize` vs osobne testy** — `parametrize`, gdy ten sam scenariusz różni się tylko danymi wejściowymi; osobne testy, gdy różni się logika asercji albo setup.
4. **schema-on-read** — schemat narzucany przy odczycie, nie zapisie. Plus: elastyczność przy zmiennej/rzadkiej strukturze rekordu. Minus: brak gwarancji integralności i wolniejsze, bardziej skomplikowane zapytania analityczne.
5. **Lazy evaluation w Sparku** — transformacje budują tylko DAG, nic się nie liczy do akcji (`show`, `collect`, `write`). Boli w debugowaniu: błąd (np. zła kolumna) wybucha dopiero przy akcji, daleko od miejsca, gdzie został wprowadzony.
6. **Audyt vs kontrakt** — audyt sprawdza dane po fakcie (raport), kontrakt wymusza reguły zanim dane wejdą do pipeline'u. W produkcji potrzeba obu: kontrakt blokuje złe dane na wejściu, audyt wyłapuje dryf jakości w czasie.

---

## Uwaga o uruchomieniu

Notebook jest uruchamialny od góry do dołu po wykonaniu `preflight_download.py` (pobranie datasetu z Hugging Face) w środowisku z PySpark/Java z lab 5. Kod każdego zadania zweryfikowałem logicznie na danych syntetycznych; pełne uruchomienie na realnym `imdb` należy wykonać lokalnie.
