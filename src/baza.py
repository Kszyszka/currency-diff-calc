'''Moduł służący do obsługi baz danych.'''
from tinydb import TinyDB, Query
from tabulate import tabulate

# Globalna deklaracja baz
db_faktury = TinyDB("data/faktury.json")
db_wplaty = TinyDB("data/wplaty.json")

def id_faktury():
    '''Obsługuje pustą bazę, zwraca ostatnie ID faktury (klucz podstawowy).'''
    # Zwraca ID ostatniej faktury, w celu ustalenia klucza podstawowego nowej faktury.
    # Przy pustej bazie, ustawia rekord zerowy, aby pierwszy poprawny rekord miał ID=1
    if len(db_faktury.all()) == 0:
        db_faktury.insert({"id_faktury": 0, "firma": "", "waluta": "", "data": "", "kwota_naleznosci": 0, "status_platnosci": 0, "kurs_waluty": 0})
    return db_faktury.all()[-1]['id_faktury'] + 1

def id_wplaty():
    '''Obsługuje pustą bazę, zwraca ostatnie ID wpłaty (klucz podstawowy).'''
    # Zwraca ID ostatniej wpłaty, w celu ustalenia klucza podstawowego nowej wpłaty.
    # Przy pustej bazie, ustawia rekord zerowy, aby pierwszy poprawny rekord miał ID=1
    if len(db_wplaty.all()) == 0:
        db_wplaty.insert({"id_wplaty": 0, "id_faktury": 0, "wartosc_wplaty": 0, "waluta": "", "data": "", "kurs": 0, "wartosc_wplaty_pln": 0})
    return db_wplaty.all()[-1]['id_wplaty'] + 1

# Funkcje zapisz(), wywoływane są jedynie po wcześniejszej walidacji zapisywanych obiektów.
def zapisz_fakture(faktura):
    '''Zapis faktury do bazy db_faktury.'''
    db_faktury.insert(faktura)

def zapisz_wplate(wplata):
    '''Zapis wpłaty do bazy db_wplaty.'''
    db_wplaty.insert(wplata)

def oplac_fakture(id_faktury_oplacana, wplata, wplata_pln, waluta, data, kurs):
    '''Opłacenie faktury o wartość wpłaty po jej zapisie do bazy. Wyliczenie róznic.'''

    # Wyszukaj fakturę i status jej opłacenia w PLN.
    faktura = Query()
    rekord = db_faktury.search(faktura.id_faktury == id_faktury_oplacana)[0]
    status_platnosci = rekord["status_platnosci"]

    # Zmniejsz należność na fakturze w bazie o wartość wpłaty w przeliczeniu na PLN.
    print(f"Kwota przed opłatą: {status_platnosci} po przeliczeniu na PLN.")
    status_platnosci = round(status_platnosci - wplata_pln, 2)
    db_faktury.update({"status_platnosci": status_platnosci}, faktura.id_faktury == id_faktury_oplacana)

    print(f"Opłacono: {wplata} {waluta}, w przeliczeniu: {wplata_pln} PLN po kursie {kurs} w dniu {data}.")
    print(f"Kwota po opłacie: {status_platnosci} po przeliczeniu na PLN.")

    # Faktura nie musi być opłacana w walucie, w której jest wystawiona.
    # Program akceptuje opłacanie w dowolnej dopuszczonej walucie.
    # Jeśli waluta spłaty = waluta faktury, wypisywane są ich różnice kursowe.
    if rekord["waluta"] == waluta:
        tabela = [["Data faktury", "Data wpłaty", "Waluta", "Różnica kursowa"],
                  [rekord["data"], data, waluta, "X"],
                  [rekord["kurs_waluty"], kurs, waluta, rekord["kurs_waluty"] - kurs]]
        print("Faktura opłacona w tej samej walucie, różnica kursowa wynosi:")
        print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'), "\n")
    else:
        print("Wpłata została wykonana w innej walucie niż podana na fakturze. Zostanie opłacona zgodnie z jej kursem, jednak niemożliwe jest wyliczenie róznic kursowych.\n")

def usun_wplate(id_wplaty_do_usuniecia):
    '''Usunięcie wpłaty o podanym ID i przywrócenie jej wartości do odpowiedniej faktury.'''

    # Znalezienie odpowiadającej wpłacie faktury
    faktura = Query()
    wplata = Query()
    wynik = db_wplaty.search(wplata.id_wplaty == id_wplaty_do_usuniecia)[0]
    if wynik:
        wartosc = wynik["wartosc_wplaty_pln"]
        id_faktury_wynik = wynik["id_faktury"]
        # Obliczenie wartości faktury po cofnięciu wpłaty i update na bazie.
        status_platnosci_new = db_faktury.search(faktura.id_faktury == id_faktury_wynik)[0]["status_platnosci"] + wartosc
        db_faktury.update({"status_platnosci": status_platnosci_new}, faktura.id_faktury == id_faktury_wynik)
        print(f"Wpłata {id_wplaty_do_usuniecia} o wartości {wartosc} PLN została usunięta. Należność została przywrócona do Faktury {id_faktury_wynik}.")
        db_wplaty.remove(wplata.id_wplaty == id_wplaty_do_usuniecia)
        return 1
    else:
        print("Wpłata nie została usunięta.")
        return 0

def wyczysc_baze_faktur():
    '''Wyczyszczenie całej bazy faktur.'''

    decyzja = input("Czy na pewno chcesz wyczyścić bazę faktur? (TAK/NIE): ").lower()
    if decyzja == "tak":
        db_faktury.truncate()
        print("Baza db_faktury (faktury.json) została wyczyszczona.\n")
    else:
        print("Baza NIE została wyczyszczona.\n")
def wyczysc_baze_wplat():
    '''Wyczyszczenie całej bazy wpłat.'''

    decyzja = input("Czy na pewno chcesz wyczyścić bazę wpłat? (TAK/NIE): ").lower()
    if decyzja == "tak":
        db_wplaty.truncate()
        print("Baza db_wplaty (wplaty.json) została wyczyszczona.\n")
    else:
        print("Baza NIE została wyczyszczona.\n")

def wyszukaj_fakture(id_faktury_szukana):
    '''Wyszukanie konkretnej faktury po jej ID.'''
    faktura = Query()
    return db_faktury.search(faktura.id_faktury == id_faktury_szukana)

def wyszukaj_fakture_nazwa(nazwa_firmy):
    '''Wyszukanie wszystkich faktur konkretnej firmy (po nazwie firmy).'''
    faktura = Query()
    return db_faktury.search(faktura.firma == nazwa_firmy)

def wyszukaj_wplate(id_wplaty_szukana):
    '''Wyszukanie konkretnej wpłaty po jej ID.'''
    wplata = Query()
    return db_wplaty.search(wplata.id_wplaty == id_wplaty_szukana)

def wyszukaj_wplate_id_faktury(id_faktury_szukana):
    '''Wyszukanie wszystkich wpłat do podanej faktury (po jej ID).'''
    wplata = Query()
    return db_wplaty.search(wplata.id_faktury == id_faktury_szukana)

def wszystkie_faktury():
    '''Wypisanie wszystkich faktur w bazie.'''
    return db_faktury.all()[1:]
