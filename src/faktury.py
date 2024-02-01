'''Moduł służący do obsługi faktur.'''
from datetime import datetime
from tabulate import tabulate
import baza
import waluty

class Faktura:
    '''Klasa reprezentująca konkretną fakturę.'''

    def __init__(self, firma, waluta, data, kwota_naleznosci) -> None:
        self.id_faktury = 1
        self.firma = firma
        self.waluta = waluta
        self.data = data
        self.kwota_naleznosci = kwota_naleznosci
        self.kurs_waluty = 0
        self.status_platnosci = 0

    def zapisz_fakture(self):
        '''Uzupełnienie atrybutów zależnych od innych modułów i zapisanie faktury do bazy.'''

        setattr(self, "id_faktury", baza.id_faktury())
        setattr(self, "kurs_waluty", waluty.Waluta(self.waluta, self.data).rate)
        setattr(self, "status_platnosci", round(self.kwota_naleznosci * self.kurs_waluty, 2))

        if self.kurs_waluty != 0:
            faktura_rekord = vars(self)
            baza.zapisz_fakture(faktura_rekord)
            print(f"Zapisana faktura ma identyfikator: {self.id_faktury}")
        else:
            print("Niepoprawna data lub kod waluty.\nFaktura nie została zapisana.")


    def czy_oplacona(self):
        '''Wypisz status opłacenia faktury.'''

        print(f"Do zapłaty zostało: {self.status_platnosci}.")
        if self.status_platnosci == 0:
            print(f"Faktura {self.id_faktury} jest opłacona. Nie zostało nic do spłaty.\n")
            return 1
        elif self.status_platnosci > 0:
            print(f"Faktura {self.id_faktury} NIE jest opłacona, zostało {self.status_platnosci} PLN do zapłaty.\n")
            return 0
        elif self.status_platnosci < 0:
            print(f"Faktura {self.id_faktury} jest nadpłacona o {self.status_platnosci*-1} PLN.\n")
        return None

    def is_valid(self):
        '''Walidacja wszystkich wprowadzonych pól wpłaty.'''

        if not self.firma:
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

def wprowadzenie_faktury():
    '''Wprowadzenie wpłaty i walidacja danych w trybie interaktywnym.'''

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

def wprowadzenie_faktury_z_pliku(nazwa_firmy, waluta, data, kwota_naleznosci):
    '''Wprowadzenie wpłaty i walidacja danych w trybie wsadowym z pliku.'''

    faktura = Faktura(nazwa_firmy, waluta, data, kwota_naleznosci)
    if faktura.is_valid():
        faktura.zapisz_fakture()
    return faktura

def wyszukaj_fakture_po_id():
    '''Wyszukaj konkretną fakturę w bazie po jej ID.'''

    try:
        id_faktury = int(input("Wprowadź ID wyszukiwanej Faktury: ").strip())
    except ValueError:
        print("Zły identyfikator Faktury.")
        return 0
    wynik = baza.wyszukaj_fakture(id_faktury)
    if wynik:
        faktura = Faktura(wynik[0]["firma"], wynik[0]["waluta"], wynik[0]["data"], wynik[0]["kwota_naleznosci"])
        setattr(faktura, "id_faktury", wynik[0]["id_faktury"])
        setattr(faktura, "kurs_waluty", wynik[0]["kurs_waluty"])
        setattr(faktura, "status_platnosci", wynik[0]["status_platnosci"])
        tabela = [["id_faktury", "firma", "waluta", "data", "kurs_waluty", "status_platnosci_pln"],
                  [faktura.id_faktury, faktura.firma, faktura.waluta, faktura.data, faktura.kurs_waluty, str(faktura.status_platnosci) + " PLN"]]
        print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'), "\n")
        return faktura
    else:
        print("Nie znaleziono Faktury o podanym ID.")

def wyszukaj_fakture_po_nazwie():
    '''Wyszukaj wszystkie faktury w bazie po nazwie ich firmy.'''

    nazwa = input("Wprowadź nazwę firmy szukanej Faktury: ").strip().capitalize()
    wynik = baza.wyszukaj_fakture_nazwa(nazwa)
    tabela = [["id_faktury", "firma", "waluta", "data", "kurs_waluty", "status_platnosci_pln"]]
    if wynik:
        for i in wynik:
            tabela2 = [i["id_faktury"], i["firma"], i["waluta"], i["data"], i["kurs_waluty"], str(i["status_platnosci"]) + " PLN"]
            tabela.append(tabela2)
        print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'), "\n")
    else:
        print("Nie znaleziono Faktury o podanej nazwie firmy.")

def wypisz_wszystkie():
    '''Wypisz wszystkie faktury w bazie faktur.'''

    faktury = baza.wszystkie_faktury()
    tabela = [["id_faktury", "firma", "waluta", "data", "kwota_naleznosci", "kurs_waluty", "status_platnosci_pln"]]
    for faktura in faktury:
        tabela2 = [faktura["id_faktury"], faktura["firma"], faktura["waluta"], faktura["data"], faktura["kwota_naleznosci"], faktura["kurs_waluty"], str(faktura["status_platnosci"]) + " PLN"]
        tabela.append(tabela2)
    print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'), "\n")

def status_platnosci_po_id():
    '''Funkcja wypisująca status opłacenia faktury ad hoc.'''

    faktura = wyszukaj_fakture_po_id()
    faktura.czy_oplacona()
