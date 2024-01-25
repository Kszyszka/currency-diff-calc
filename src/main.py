from datetime import datetime

class Faktura:
    def __init__(self,firma, waluta, data, kwota_naleznosci) -> None:
        self.id_faktury = None
        self.firma = firma
        self.waluta = waluta
        self.data = data
        self.kwota_naleznosci = kwota_naleznosci
        self.status_platnosci = kwota_naleznosci
        setattr(self, 'id_faktury', None) # Przyda się przy tworzeniu bazy faktur
        
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
        if any(char.isdigit() for char in self.waluta) or len(self.waluta) != 3:
            print("Niepoprawna waluta (IS0 4217).")
            return 0
        if not self.data:
            print("Data nie może być pusta.")
            return 0
        if not self.kwota_naleznosci and self.kwota_naleznosci != 0:
            print("Kwota należności nie może być pusta.")
            return 0
        try:
            datetime.strptime(self.data, "%Y-%m-%d")
        except ValueError:
            print("Niepoprawna data, powinna być w formacie YYYY-MM-DD.")
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
    print("\nWprowadz dane nowej faktury rozdzielone ';' lub w osobnych linijkach:")
    print("Firma; Waluta faktury; Data wystawienia; Kwota należności")
    dane_faktury = []
    wprowadzone_dane = input("\nNazwa firmy lub dane rozdzielone ';': ")
    if ';' in wprowadzone_dane:
        dane_faktury = [i.strip() for i in wprowadzone_dane.split(';')]
        dane_faktury[0].strip().capitalize()
        dane_faktury[1].strip().upper()
        dane_faktury[3] = float(dane_faktury[3])
    else:
        dane_faktury.append(wprowadzone_dane.strip().capitalize())
        dane_faktury.append(input("Waluta faktury: ").upper())
        dane_faktury.append(input("Data wystawienia: "))
        dane_faktury.append(input("Kwota należności: "))
    return dane_faktury
        


def main():
    test = Faktura("Biedronka", "PLN", "2024-01-31", "2137")
    while True:
        test = wprowadzenie_faktury()
        faktura = Faktura(test[0], test[1], test[2], test[3])
        if faktura.is_valid():
            break
    faktura.czy_oplacona()
       
if __name__ == "__main__":
    main()