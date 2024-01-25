import requests
from datetime import datetime

class Waluta:
    def __init__(self, code, data):
        self.code = code.strip().upper()
        self.data = data.strip()
        url = f"http://api.nbp.pl/api/exchangerates/rates/C/{self.code}/{self.data}/"
        r = requests.get(url, headers={"Accept": "application/json"})
        print(r.status_code)
        if r.status_code == 200:
            self.rate = float(r.json()["rates"][0]["bid"]) # Kurs sprzedaży
        else:
            print("Błędnie podany kod waluty lub data kursu - błąd połączenia z API.")
            self.rate = None
    def is_valid(self):
        if len(self.code) != 3:
            print("Zły kod waluty.")
            return 0
        try:
            datetime.strptime(self.data, "%Y-%m-%d")
        except ValueError:
            print("Zły format daty.")
            return 0
        if self.rate == None:
            print("Niepoprawny kurs waluty - problem połączenia z API.")
            return 0
        return 1
    def show(self):
        # Pretty print?
        print(f"kod\tdata\tkurs")
        print(f"{self.code}\t{self.data}\t{self.rate}")

def wprowadzenie_waluty():
    print("\nWprowadz dane kursu waluty rozdzielone ';' lub w osobnych linijkach:")
    print("Kod waluty (ISO 4217); Data w formacie 'YYYY-MM-DD")

def main():
    waluta = Waluta(" USD ", " 2020-10-14")

    waluta.show()

if __name__ == "__main__":
    main()