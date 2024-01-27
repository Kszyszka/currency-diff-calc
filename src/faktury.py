from datetime import datetime
import baza, waluty

class Faktura:
    def __init__(self, firma, waluta, data, kwota_naleznosci) -> None:
        self.id_faktury = 1
        self.firma = firma
        self.waluta = waluta
        self.data = data
        self.kwota_naleznosci = kwota_naleznosci
        self.kurs_waluty = 0
        self.status_platnosci = 0
        
    def zapisz_fakture(self):
        setattr(self, "id_faktury", baza.id_faktury())
        setattr(self, "kurs_waluty", waluty.Waluta(self.waluta, self.data).rate)
        setattr(self, "status_platnosci", self.kwota_naleznosci * self.kurs_waluty)

        faktura_rekord = vars(self)
        baza.zapisz_fakture(faktura_rekord)
        print(f"Zapisana faktura ma identyfikator: {self.id_faktury}")
        
    def czy_oplacona(self):
        if self.status_platnosci == 0:
            print(f"Faktura {self.id_faktury} jest opłacona.")
            return 1
        elif self.status_platnosci > 0:
            print(f"Faktura {self.id_faktury} NIE jest opłacona, zostało {self.status_platnosci} {self.waluta} do zapłaty.")
            return 0
        elif self.status_platnosci < 0:
            print(f"Faktura {self.id_faktury} jest nadpłacona o {self.status_platnosci*-1} {self.waluta}.")
        return None
        
    def is_valid(self):
        print("\n")
        if not self.firma.strip():
            print("Nazwa firmy nie może być pusta")
            return 0
        if self.waluta not in ["USD", "EUR", "GBP"]:
            print("Niepoprawna waluta (IS0 4217). Program obsługuje waluty: USD, EUR, GBP.")
            return 0
        if not self.data:
            print("Data nie może być pusta.")
            return 0
        try:
            datetime.strptime(self.data, "%Y-%m-%d")
        except ValueError:
            print("Niepoprawna data, powinna być w formacie YYYY-MM-DD.")
            return 0
        if not self.kwota_naleznosci and self.kwota_naleznosci != 0:
            print("Kwota należności nie może być pusta.")
            return 0
        try:
            self.kwota_naleznosci = float(self.kwota_naleznosci)
            self.status_platnosci = float(self.status_platnosci)
        except ValueError:
            print("Niepoprawna kwota faktury.")
            return 0
        return 1
    
    def show(self):
        # Pretty print?
        print("id\tfirma\twaluta\tdata\tnaleznosc\tzostalo")
        print(f"{self.id_faktury}\t{self.firma}\t{self.waluta}\t{self.data}\t{self.kwota_naleznosci}\t{self.status_platnosci}")
        
    #TODO status faktury, spłacanie, id faktury z pliku
    
def wprowadzenie_faktury():
    while True:
        print("\nWprowadz dane nowej faktury w osobnych linijkach:")
        print("Firma; Waluta faktury; Data wystawienia (YYYY-MM-DD); Kwota należności")
        dane_faktury = []
        
        dane_faktury.append(input("\nNazwa firmy: ").strip().capitalize())
        dane_faktury.append(input("Waluta faktury: ").strip().upper())
        dane_faktury.append(input("Data wystawienia: ").strip())
        dane_faktury.append(input("Kwota należności: ").strip())
        
        faktura = Faktura(dane_faktury[0], dane_faktury[1], dane_faktury[2], dane_faktury[3])
        if faktura.is_valid():
            faktura.zapisz_fakture()
            break
    return faktura
        


def main():
    faktura = wprowadzenie_faktury()
    
    faktura.show()
       
if __name__ == "__main__":
    main()