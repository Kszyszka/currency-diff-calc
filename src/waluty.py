import requests
from datetime import datetime
from tabulate import tabulate

class Waluta:
    def __init__(self, code, data):
        self.code = code.strip().upper()
        self.data = data.strip()
        
        url = f"http://api.nbp.pl/api/exchangerates/rates/C/{self.code}/{self.data}/"
        r = requests.get(url, headers={"Accept": "application/json"})
        global status_polaczenia
        status_polaczenia = r.status_code

        if status_polaczenia == 200:
            self.rate = float(r.json()["rates"][0]["bid"]) # Kurs sprzedaży
        elif status_polaczenia == 404:
            print("Błędna data - brak kursu.")
            self.rate = 0            
        else:
            print(f"Błędnie podany kod waluty lub za duży zakres danych - błąd połączenia z API.{status_polaczenia}")
            print(url)
            self.rate = 0

    def is_valid(self):
        if self.code not in ["USD", "EUR", "GBP"]:
            print("Niepoprawna waluta (IS0 4217). Program obsługuje waluty: USD, EUR, GBP.")
            return 0
        try:
            datetime.strptime(self.data, "%Y-%m-%d")
        except ValueError:
            print("Niepoprawna data, powinna być w formacie YYYY-MM-DD.")
            return 0
        return 1
        
def wprowadzenie_waluty():
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
    print("Pierwsza waluta:")
    waluta_pierwsza = wprowadzenie_waluty()
    print("\nDruga waluta:")
    waluta_druga = wprowadzenie_waluty()
    if waluta_pierwsza.code == waluta_druga.code:
        if waluta_pierwsza.rate == 0 or waluta_druga.rate == 0:
            print("Jedna z podanych walut lub dat jest błędna, błąd API.")
        else:
            tabela = [["Data1", "Data2", "Waluta", "Różnica kursowa"],
                    [waluta_pierwsza.data, waluta_druga.data, waluta_pierwsza.code, "X"],
                    [waluta_pierwsza.rate, waluta_druga.rate, waluta_pierwsza.code, waluta_pierwsza.rate - waluta_druga.rate]]
            print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'),"\n")
    else:
        print("Podane zostały różne waluty, nie można wyliczyć różnicy kursowej.\n")
        
def konkretna_data():
    waluta = wprowadzenie_waluty()
    tabela = [["Data", "Waluta", "Kurs"],
              [waluta.data, waluta.code, waluta.rate]]
    print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'),"\n")