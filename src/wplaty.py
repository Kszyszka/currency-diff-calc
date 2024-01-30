from datetime import datetime
import baza, waluty

class Wplata:
    def __init__(self, id_faktury, wartosc_wplaty, waluta, data):
        self.id_wplaty = 1
        self.id_faktury = id_faktury
        self.wartosc_wplaty = wartosc_wplaty
        self.waluta = waluta
        self.data = data
        self.kurs = 0
    
    def is_valid(self):
        print("\n")
        if not self.id_faktury or self.id_faktury == 0:
            print("ID faktury nie może być puste.")
            return 0
        try:
            self.id_faktury = int(self.id_faktury)
        except ValueError:
            print("Niepoprawne ID faktury.")
            return 0
        if baza.wyszukaj_fakture(self.id_faktury) == []:
            print("Nie istnieje faktura o podanym ID.")
            return 0
        if not self.wartosc_wplaty or self.wartosc_wplaty == 0:
            print("Wartość płaty nie może być pusta.")
            return 0
        try:
            self.wartosc_wplaty = float(self.wartosc_wplaty)
            self.wartosc_wplaty = float(self.wartosc_wplaty)
        except ValueError:
            print("Niepoprawna kwota faktury.")
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
        return 1
    
    def zapisz_wplate(self):
        setattr(self, "id_wplaty", baza.id_wplaty())
        setattr(self, "kurs", waluty.Waluta(self.waluta, self.data).rate)
        setattr(self, "wartosc_wplaty_pln", round(self.wartosc_wplaty * self.kurs, 2))

        wplata_rekord = vars(self)
        baza.zapisz_wplate(wplata_rekord)
        print(f"Zapisana wpłata ma identyfikator: {self.id_wplaty}")
    
def wprowadzenie_wplaty():
    while True:
        print("\nWprowadz dane wplaty w osobnych linijkach:")
        print("Id oplacanej faktury; Wartosc wplaty; Waluta wplaty; Data wystawienia (YYYY-MM-DD).")
        dane_wplaty = []
        
        dane_wplaty.append(input("\nID faktury: ").strip())
        dane_wplaty.append(input("Wartosc wplaty: ").strip())
        dane_wplaty.append(input("Waluta wplaty: ").strip().upper())
        dane_wplaty.append(input("Data wplaty: ").strip())
        
        wplata = Wplata(dane_wplaty[0], dane_wplaty[1], dane_wplaty[2], dane_wplaty[3])
        if wplata.is_valid():
            wplata.zapisz_wplate()
            baza.oplac_fakture(wplata.id_faktury, wplata.wartosc_wplaty_pln)
            break
    return wplata