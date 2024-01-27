import requests
from datetime import datetime

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
            print("Data wskazuje na dzień wolny - brak kursu.")
            self.rate = 0            
        else:
            print(f"Błędnie podany kod waluty lub za duży zakres danych - błąd połączenia z API.{status_polaczenia}")
            print(url)
            self.rate = 0

    def show(self):
        # Pretty print?
        print(f"kod\tdata\tkurs")
        print(f"{self.code}\t{self.data}\t{self.rate}")

def wprowadzenie_waluty(kod, data):
    waluta = Waluta(kod, data)
    return waluta

def main():
    waluta = Waluta(" USD ", " 2020-10-14")

    waluta.show()

if __name__ == "__main__":
    main()