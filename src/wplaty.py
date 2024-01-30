from datetime import datetime
import baza, waluty
from tabulate import tabulate

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
            baza.oplac_fakture(wplata.id_faktury, wplata.wartosc_wplaty, wplata.wartosc_wplaty_pln, wplata.waluta, wplata.data, wplata.kurs)
            break
    return wplata

def wyszukaj_wplate_po_id():
    try:
        id = int(input("Wprowadź ID wyszukiwanej Wpłaty: ").strip())
    except ValueError:
        print("Zły identyfikator Wpłaty.")
        return 0
    wynik = baza.wyszukaj_wplate(id)
    if len(wynik) != 0:
        wplata = Wplata(wynik[0]["id_faktury"], wynik[0]["wartosc_wplaty"], wynik[0]["waluta"], wynik[0]["data"])
        setattr(wplata, "id_wplaty", wynik[0]["id_wplaty"])
        setattr(wplata, "kurs", wynik[0]["kurs"])
        setattr(wplata, "wartosc_wplaty_pln", wynik[0]["wartosc_wplaty_pln"])
        print(vars(wplata))
        return wplata
    else:
        print("Nie znaleziono Wpłaty o podanym ID.")
        
def wyszukaj_wplate_po_id_faktury():
    try:
        id = int(input("Wprowadź ID wyszukiwanej Faktury poszukiwanych wpłat: ").strip())
    except ValueError:
        print("Zły identyfikator Faktury.")
        return 0
    wynik = baza.wyszukaj_wplate_id_faktury(id)
    if wynik:
        for i in wynik:
            wplata = Wplata(i["id_faktury"], i["wartosc_wplaty"], i["waluta"], i["data"])
            setattr(wplata, "id_wplaty", i["id_wplaty"])
            setattr(wplata, "kurs", i["kurs"])
            setattr(wplata, "wartosc_wplaty_pln", i["wartosc_wplaty_pln"])
            print(vars(wplata))
    else:
        print("Nie znaleziono Wpłat o podanym ID Faktury.")
        return 0
    return 1

def usun_wplate():
    try:
        id = int(input("Wprowadź ID wyszukiwanej Wpłaty: ").strip())
    except ValueError:
        print("Zły identyfikator Wpłaty.")
        return 0
    wynik = baza.usun_wplate(id)
    if not wynik:
        print("Nie znaleziono Wpłaty o podanym ID.")
        
def roznice_kursowe():
    wplata = wyszukaj_wplate_po_id()
    if wplata:
        faktura = baza.wyszukaj_fakture(wplata.id_faktury)[0]
    
        if wplata.waluta == faktura["waluta"]:
            tabela = [["Data faktury", "Data wpłaty", "Waluta", "Różnica kursowa"],
                    [faktura["data"], wplata.data, wplata.waluta, "X"],
                    [faktura["kurs_waluty"], wplata.kurs, wplata.waluta, faktura["kurs_waluty"] - wplata.kurs]]
            print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'))
        else:
            print("Wybrana wpłata oraz faktura są w innych walutach, nie da się wyliczyć różnic kursowych.")