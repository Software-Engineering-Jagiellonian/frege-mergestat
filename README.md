# MERGESTAT

## Czym jest mergestat:
Mergestat jest narzędziem umożliwiającym analizę repozytorium (w tym rzecz jasna commitów, ich treści,  plików, ich zmian, autorów etc.) wykorzystującym przy tym wygodną i prostą w obsłudze składnię języka SQL. Ponadto mergestat dostarcza również niewielki zbiór gotowych do wykorzystania w zapytaniach metod rozszerzających funkcjonalność samego języka SQL. Jednakże to właśnie możliwość wykorzystania składni SQL jest główną zaletą narzędzia mergestat, a zatem na nim oraz możliwości jego zastosowania na dalszym etapie rozwoju projektu FREGE opierał się będzie owy artykuł. Kwestia gotowych metod dostarczanych przez mergestat traktowana jest drugorzędnie. Zainteresowanych odsyłam do dokumentacji.

W praktyce narzędzie mergestat mapuje repozytorium (dane pochodzące z systemu kontroli wersji + treści commitowanych plików) na zbiór tabel. Wykorzystaną przy tym bazą danych jest baza SQLite. Zbiór tabeli jakimi dysponuje mergestat zamieszczony został w sekcji *Generowane tabele*

## Przydatne linki:
Dokumentacja: https://docs.mergestat.com/ \
Repozytorium: https://github.com/mergestat/mergestat \
Obraz dockerowy: https://hub.docker.com/r/mergestat/mergestat \
Sandbox: https://app.mergestat.com/w/public \
Repozytorium frege: https://github.com/Software-Engineering-Jagiellonian

## Uwaga:
Wszystkie poniżej zamieszczone przykłady zakładają istnienie repozytorium https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git W przypadku np. przyszłej zmiany nazwy repozytorium użytkownik może otrzymać informację o braku istnienia repozytorium. Należałoby wtedy podmienić adres repozytorium na właściwy. Zachęcam rówież do samodzielnego uruchamiania przykładów również na innych repozytoriach.

## Generowane tabele:
Przed szczegółowym zapoznaniem się z generowanymi przez narzędzie mergestat tabelami polecaną rzeczą jest przejście przez przygotowany w sekcji *Tutorial* kurs obsługi narzędzia mergestat bądź też zapoznawanie się z ową sekcją równolegle podczas wykonywania poleceń z zekcji *Tutorial*. Pozwala ona oswoić się z narzędziem mergestat oraz jego możliwościami. Sekcja *Tutorial* korzysta z poniższych tabel, w związku z czym zamieszczona została nad nią. Zachęcam do tego, aby zarówno przykładowe zapytania z sekcji *Tutorial*, jak również przykłady użycia poniższych tabel, przetestować wykorzystując do tego sandbox z sekcji *Przydatne linki*. Pozwala to jeszcze bardziej zapoznać się z narzędziem oraz zwizualizować postać zwracanych danych. Ze względu na intuicyjne nazwy pól poszczególnych tabel zbędne komentowanie ich zastosowania zostało pominięte.

### commits
Zawartość tabeli:

| hash    | message  | author_name | author_email | author_when | committer_name | committer email | committer_when | parents |
|---------|----------|-------------|--------------|-------------|----------------|-----------------|----------------|---------|
| TEXT    | TEXT     | TEXT        | TEXT         | DATETIME    | TEXT           | TEXT            | DATETIME       | INT     |

Składnia

*commits(\<REPOSITORY\>, \<LAST_COMMIT\>)*
1. \<REPOSITORY\> - Adres repozytorium (domyślnie lokalne repozytorium spod katalogu */repo*)
2. \<LAST_COMMIT\> - Adres commita, do którego zwrócić wyniki (domyśla wartość HEAD)

Przykład użycia:
```shell
Select * from commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
```

### refs
Zawartość tabeli:

| name | type | remote | full_name | hash | target |
|------|------|--------|-----------|------|--------|
| TEXT | TEXT | TEXT   | TEXT      | TEXT | TEXT   |

Składnia

*refs(\<REPOSITORY\>)*
1. \<REPOSITORY\> - Adres repozytorium (domyślnie lokalne repozytorium spod katalogu */repo*)

Przykład użycia:
```shell
Select * from refs('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
```

### stats
Zawartość tabeli:

| file_path | additions | deletions |
|-----------|-----------|-----------|
| TEXT      | INT       | INT       |

Składnia

*stats(\<REPOSITORY\>, \<REV\>, \<TO_REV\>)*
1. \<REPOSITORY\> - Adres repozytorium (domyślnie lokalne repozytorium spod katalogu */repo*)
2. \<REV\> - Commit hash / branch name / tag name (domyślnie HEAD)
3. \<TO_REV\> - Rev, z którym chcemy porównać rezultat (domyślnie od początku)

Przykład użycia:
```shell
Select * from stats('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git', '7c27c46624639a9381659973d104e680d4c4dcf3', 'c63dd31f5e5ef9c3918848d2714d8e751d13cecf')
```

### files
Zawartość tabeli:

| path | executable | contents |
|------|------------|----------|
| TEXT | BOOL       | TEXT     |

Składnia

*files(\<REPOSITORY\>, \<REV\>)*
1. \<REPOSITORY\> - Adres repozytorium (domyślnie lokalne repozytorium spod katalogu */repo*)
2. \<REV\> - Commit hash / branch name / tag name, z którego pochodzić mają pliki (domyślnie HEAD)

Przykład użycia:
```shell
Select * from files('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
```

### blame
Zawartość tabeli:

| line_no | commit_hash |
|---------|-------------|
| INT     | TEXT        |

Składnia

*blame(\<REPOSITORY\>, \<REV\>, \<FILE_PATH\>)*
1. \<REPOSITORY\> - Adres repozytorium (domyślnie lokalne repozytorium spod katalogu */repo*)
2. \<REV\> - Commit hash / branch name / tag name, z którego pochodzić ma plik (domyślnie HEAD)
3. \<FILE_PATH\> - nazwa pliku

Przykład użycia:
```shell
SELECT * FROM blame('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git', 'HEAD', 'README.md')
```

## Tutorial:
Dalsza część owego wpisu pozwalającego w szybki sposób zapoznać się z narzędziem mergestat oraz możliwościami wykorzystania go w projekcie FREGE przedstawiona zostanie w formie krótkiego tutorialu pozwalającego na obycie się z owym narzędziem oraz inspirującego do dalszych poczynań z jego wykorzystaniem. Sposób ten wydaje się zarówno obniżać próg wejścia w obsługę narzędzia, jak również pozwala zobaczyć działanie narzędzia w praktyce. \

Uruchommy obraz dockerowy mergestat. Oczekuje on na wejściu polecenie jakie ma wykonać. Na wstępie zapoznajmy się z manualem narzędzia (flag -h na wejściu). Kontener wypisuje na standardowe wyjście informacje o sposobie użycia, komendach oraz flagach jakimi dysponuje
```shell
docker run mergestat/mergestat -h
```
- Default current working directory / --repo
- --format json / csv

Jak możemy przeczytać w manualu mergestat może być użytkowany na 2 sposoby:
1. W formie zapytania SQL:
```shell
mergestat "SELECT * FROM <TABLE_NAME>" [flags]
```
2. Oraz w formie wykonania innego polecenia z listy dostępnych poleceń:
```shell
mergestat [command]
```
Sprawdźmy zatem sposób działania przykładowej komendy *summarize*. Zwróci ono podsumowanie naszego projektu. Zanim natomiast wykorzystamy ową komendę zapoznajmy się z jej manualem:
```shell
docker run mergestat/mergestat summarize -h
```
Dowiadujemy się z niego, iż mergestat dysponuje możliwością podsumowania projektu w zakresie:
1. *commits* - informacje m.in. o liczbie commitów poszczególnych autorów, ich procentowym udziale wśród wszystkich zmian, delcie zmian, pierwszym i ostatnim commicie
2. *blame* - analogicznie jak dla commitów, podsumowanie m.in. liczby zmian poszczególnych autorów, procentowy udział, oraz dacie pierwszej i ostatniej zmiany danego pliku

Jako, że na etapie uruchamiania obrazu nie został podany wolumen z lokalnie sklonowanym repozytorium, powyższy przykład, jak również przykłady użycia tabel w sekcji *Generowane tabele* wymagały w sposób jawny podania adresu repozytorium, na którym mergestat wykonać ma dane polecenie. W przeciwnym wypadku otrzymamy informację o błędzie próby odczytania repozytorium z katalogu /repo. W przypadku zapytań SQL, był to jak mogliśmy zauważyć w sekcji *Generowane tabele* 1. parametr danej tabeli w zapytaniu (jeżeli wszystkie parametry są domyślne, natomiast analizowane repo znajduje się pod adresem /repo nawiasy z na parametry całkowicie mogą zostać pominięte). Dla pozostałych komend, jak podaje manual, jawnemu definiowaniu repozytorium służy flaga -r.

Sprawdźmy zatem podsumowanie commitów naszego projektu:
```shell
docker run mergestat/mergestat summarize commits -r 'https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git'
```

Analogiczne podsumowanie dla zmian pliku README.md:
```shell
docker run mergestat/mergestat summarize blame README.md -r 'https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git'
```



Standarowa, tabelaryczna odpowiedź jest czytelna dla użytkownika, natomiast bardziej przydatnym formatem w celach dalszego przetwarzania odpowiedzi jest format json/csv:
```shell
docker run mergestat/mergestat "select * from commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')" -f json
```

**Wykonajmy teraz kilka bardziej złożonych przykładów:**

*Uwaga: dalsze zapytania można wykonać przy użyciu dockera, w taki sposób, w jaki wykonywane były powyżej (docker run mergestat/mergestat "\<QUERY\>"), natomiast zachęcam do zapoznania się z sandboxem, do którego link zamieszczony został w sekcji Przydatne linki*

Stwórzmy zapytanie zliczające liczbę operacji merge. Potrzebujemy zatem skorzystać z tabeli *commits* oraz metody SQL *count*. Merge jest sytuacją gdy commit posiada więcej niż jednego rodzica, zatem licza rodziców zostanie ograniczona klaulą *WHERE*. Znając natomiast strukturę generowanych tabel (sekcja *Generowane tabele*) wiemy, iż informację tą pozyskać możemy z pola *parents* tabeli *commits*. Całość zapytania finalnie prezentować się będzie np. w następujący sposób:
```shell
SELECT hash, message, author_name, author_when, committer_email, count(*)
FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
WHERE parents > 1
```

Kolejnym zapytaniem jakie wykonamy jest zliczenie liczby operacji *commit* wykonanych przez poszczególnych użytkowników. W tym celu ponownie wykorzystamy metodę *count* dostarczaną przez bazę danych SQLite. Tym razem natomiast wyniki pogrupujemy klauzulą *GROUP BY* względem autorów. Ponadto zwracane dane posortujmy malejąco, tak, aby poznać osoby, które dokonały największej liczby commitów. Ponadto dane ograniczmy do 3 najczęściej commitujących osób:
```shell
SELECT author_name, count(*)
FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
GROUP BY author_name
ORDER BY count(*) DESC
LIMIT 3
```

Jednym z następstwem rozwoju projektu FREGE będzie zapewne analiza operacji *commit* typu FIX, BUG, etc. Zwróćmy zatem te commity, które w treści wiadomości zawierają słowa kluczowe fix lub bug:
```shell
select * from commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
where message like '%fix%' or message like '%bug%'
```

## Aplikacja narzędzia *mergestat* w projekcie FREGE
Poza pytaniami o to co oferuje *mergestat* pojawia się pytanie o to jakie są sposoby aplikacji narzędzia *mergestat* w projekcie FREGE. Poniżej omawiam następujące propozycje:
1. Publicznego API projektu
2. Obraz dockerowy

### Publiczne API:

W celu wykonania zapytania przy użyciu publicznego API projektu należy wykonać metodę https *POST* na adres *https://graphql.mergestat.com/api/rest/query*, której ciałem jest treść zapytania w postaci json (pole sql):
```shell
POST: https://graphql.mergestat.com/api/rest/query
BODY: {
    "sql": "select * from commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')"
}
```

W odpowiedzi otrzymujemy plik json, którego jednym z pól jest pole *id*. Zapytanie nasze oczekuje w kolejce na jego przetworzenie. Aby przetworzyć zapytanie należy wykonać metodę *GET* na asres *https://graphql.mergestat.com/api/rest/query-results/:ID*, gdzie w miejsce :ID należy wstawić wygenerowaną we wcześniejszym zapytaniu *POST* wartość pola *id*.
```shell
GET: https://graphql.mergestat.com/api/rest/query-results/:ID
```
W odpowiedzi otrzymujemy plik json z interesującymi nas danymi.

### Frege-mergestat:
Pierwsze z rozwiązań jest niestety rozwiązaniem ograniczonym m.in przez limit 500 wierszy w jednym zapytaniu.

W związku z czym preferowanym przeze mnie rozwiązaniem jest propozycja nr 2. Co więcej nie musi się ona ograniczać do prostego uruchamiania udostępnianego obrazu w celu każdorazowego wykonania pojedynczej operacji. Bazując na repozytorium projektu (sekcja *Przydatne linki*) można zaimplementować własne serwisy udostępniające np. customowe dla projektu FREGE API implementujące interesujące nas algorytmy analizy repozytorów.

Prosty przykład opisanego powyżej rozwiązania znaleźć można pod adresem \<TU WSTAWIĆ ADRES REPOZYTORIUM PRZYKŁADOWEGO SERWISU\>. Zachęcam do dalszej zabawy projektem, rozwoju pomysłu i implementacji przydatnych dla FREGE endpointów. Projekt rzecz jasna jest jedynie prostym POC (proof-of-concept), którego celem jest zaproponowanie jednej z metod wykorzystania narzędzia jakim jest *mergestat* oraz inspiracja do dalszego rozwoju pomysłu.

Najważniejsze informacje odnośnie przykładowego serwisu:
1. Serwis dostarczany jest w postaci obrazu dockerowego, którego szczegóły można znaleźć w pliku *Dockerfile*
2. Projekt bazuje na repozytorium *mergestat* w postaci submodułu, natomiast sam projekt *mergestat* również posiada submoduły, w związku z czym podczas klonowania repozytorium istotne jest, aby klonować je rekursywnie, w przeciwnym wypadku obraz się nie zbuduje.
3. Implementacja udostępnianego przez serwer API znajduje się w pliku *main.py*

Klonowanie, budowanie oraz uruchamianie obrazu projektu:
```shell
git clone --recursive <TU WSTAWIĆ ADRES REPOZYTORIUM PRZYKŁADOWEGO SERWISU>
cd frege-mergestat
docker build -t frege-mergestat .
docker run -d --name frege-mergestat-service -p 80:80 frege-mergestat
```

Przykłady użycia API powyżej uruchomionego serwera:
```shell
POST http://localhost/mergestat
BODY: {
    "query": "summarize commits % --start '-7 days' --repo 'https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git' --json"
}
```
```shell
POST http://localhost/mergestat
BODY: {
    "query": "\"SELECT author_name, count(*) FROM commits('https://github.com/mergestat/mergestat') WHERE parents < 2 GROUP BY author_name ORDER BY count(*) DESC\" -f json"
}
```
