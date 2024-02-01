# Currency Difference Calculator

**currency-diff-calc** - Program księgowy z obsługą obliczania różnic kursowych.\
**Autor:** Krzysztof Hager 52687

## Dokumentacja
Dokumentacja jest dostępna w zasobie ***documentation***, raport z zadania w zasobie ***raport***.

## Instalacja
Program korzysta z kilku bibliotek, które nie są wbudowane w czystego Pythona.\
- **Tabulate** - pretty print tabeli
- **TinyDB** - obsługa minimalistycznych baz danych z plików .json
- **Datetime** - walidacja wprowadzonych danych z zakresu dat
- **Requests** - obsługa API

Należy pobrać całe repozytorium, oraz pobrać powyższe zależności.\
Przed pierwszym uruchomieniem programu niezbędne jest ich zainstalowanie, poprzez wykorzystanie pliku ***"setup/requirements.txt"***:

`pip install -r setup/requirements.txt` lub `python -m pip install -r setup/requirements.txt`

## Wykorzystanie
Program działa w dwóch trybach:

1. Interaktywnym - ręczna obsługa zaawansowanych funkcji
2. Wsadowym - wykorzystanie jako komendy, masowy import faktur oraz wpłat

### Tryb Interaktywny:
Tryb interaktywny wywołuje się poprzez zwykłe uruchomienie programu, lub uruchomienie go z błędnym parametrem:

`python currency-diff-calc.py` lub np. `python currency-diff-calc.py -abcd plik.xlsx` (złe parametry)

### Tryb wsadowy
Tryb wsadowy wywołuje się poprzez uruchomienie programu wraz z jednym z argumentów:

- "-h" (--help) - wypisanie pomocy programu
- "-fF" (--fileFaktura <plik.csv>) - masowe wprowadzenie nowych faktur z pliku .csv z podanej ścieżki
- "-fW" (--fileWplata <plik.csv>) - masowe wprowadzenie nowych wpłat z pliku .csv z podanej ścieżki

Np.: `python currency-diff-calc.py -fF faktury.csv` lub `python currency-diff-calc.py -fW C:\Users\<username>\Desktop\wplaty.csv`

## Funkcjonalność
Program ma o wiele większą funkcjonalność w trybie interaktywny, jest to:

* Obsługa Faktur:
    1. Wprowadzenie nowej Faktury
    2. Wyszukanie Faktury w bazie po ID
    3. Wyszukanie Faktur w bazie po nazwie firmy
    4. Wyszukiwanie wszystkich Faktur w bazie
    5. Sprawdzenie statusu opłacenia faktury
* Obsługa Wpłat:
    1. Wprowadzenie nowej Wpłaty i opłacenie Faktury
    2. Wyszukanie Wpłaty po ID
    3. Wyszukanie Wpłaty po ID opłacanej Faktury
    4. Usunięcie Wpłaty i przywrócenie środków do Faktury
* Obliczanie Różnic Kursowych:
    1. Obliczanie różnic kursowych dla dowolonych dat
    2. Obliczanie różnic kursowych pomiędzy Fakturą a Wpłatą
    3. Sprawdzenie kursu waluty dla konkretnego dnia
* Obsługa Baz Danych:
    1. Wyczyszczenie Bazy Faktur
    2. Wyczyszczenie Bazy Wpłat


##