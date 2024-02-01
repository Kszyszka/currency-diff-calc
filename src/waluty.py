'''Moduł służący do obsługi walut oraz API.'''
from datetime import datetime
from tabulate import tabulate
import requests

class Waluta:
    '''Klasa reprezentująca konkretną walutę w dacie.'''

    def __init__(self, code, data):
        self.code = code.strip().upper()
        self.data = data.strip()

        url = f"http://api.nbp.pl/api/exchangerates/rates/C/{self.code}/{self.data}/"
        r = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
        status_polaczenia = r.status_code

        # Jeśli połączenie z API się uda, ustal kurs
        if status_polaczenia == 200:
            self.rate = float(r.json()["rates"][0]["bid"]) # Kurs sprzedaży
        elif status_polaczenia == 404:
            print("Błędna data - brak kursu.")
            self.rate = 0
        else:
            print("Błędnie podany kod waluty lub za duży zakres danych.", end=" ")
            print(f"- błąd połączenia z API.{status_polaczenia}", url)
            self.rate = 0

    def is_valid(self):
        '''Walidacja wszystkich wprowadzonych pól waluty.'''

        if self.code not in ["USD", "EUR", "GBP"]:
            print("Niepoprawna waluta (IS0 4217). Program obsługuje waluty: USD, EUR, GBP.")
            return 0
        if self.rate == 0:
            # Brak komunikatu, błąd jest raportowany w __init__
            return 0
        try:
            datetime.strptime(self.data, "%Y-%m-%d")
        except ValueError:
            print("Niepoprawna data, powinna być w formacie YYYY-MM-DD.")
            return 0
        return 1

def wprowadzenie_waluty():
    '''Wprowadzenie waluty i walidacja danych w trybie interaktywnym.'''

    while True:
        print("Wprowadz dane waluty w osobnych linijkach:")
        print("Kod waluty; Data wystawienia (YYYY-MM-DD)")
        dane_waluty = []

        dane_waluty.append(input("\nKod waluty: ").strip().upper())
        dane_waluty.append(input("Data wystawienia: ").strip())

        waluta = Waluta(dane_waluty[0], dane_waluty[1])
        if waluta.is_valid():
            break
    return waluta

def roznica_kursowa():
    '''Wyliczenie różnic kursowych tej samej waluty w różnych datach.'''

    # Wprowadzenie dwóch walut i utworzenie obiektów, walidacja w funkcji wprowadzenie
    print("Pierwsza waluta:")
    waluta_1 = wprowadzenie_waluty()
    print("\nDruga waluta:")
    waluta_2 = wprowadzenie_waluty()

    # Różnice kursowe można obliczyć tylko dla tej samej waluty
    if waluta_1.code == waluta_2.code:
        if waluta_1.rate == 0 or waluta_2.rate == 0:
            print("Jedna z podanych walut lub dat jest błędna, błąd API.")
            return 0
        else:
            tabela = [["Data1", "Data2", "Waluta", "Różnica kursowa"],
                    [waluta_1.data, waluta_2.data, waluta_1.code, "X"],
                    [waluta_1.rate, waluta_2.rate, waluta_1.code, waluta_1.rate - waluta_2.rate]]
            print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'),"\n")
            return 1
    else:
        print("Podane zostały różne waluty, nie można wyliczyć różnicy kursowej.\n")
        return 0

def konkretna_data():
    '''Wypisanie danych waluty w konkretnej dacie.'''
    # Proste wypisanie atrybutów klasy waluty, walidacja w funkcji wprowadzenie
    waluta = wprowadzenie_waluty()
    tabela = [["Data", "Waluta", "Kurs"],
              [waluta.data, waluta.code, waluta.rate]]
    print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'),"\n")
