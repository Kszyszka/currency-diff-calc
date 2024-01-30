from tinydb import TinyDB, Query
from tabulate import tabulate

db_faktury = TinyDB("data/faktury.json")
db_wplaty = TinyDB("data/wplaty.json")

if len(db_faktury.all()) == 0:
    db_faktury.insert({"id_faktury": 0, "firma": "", "waluta": "", "data": "", "kwota_naleznosci": 0, "status_platnosci": 0, "kurs_waluty": 0})
    
if len(db_wplaty.all()) == 0:
    db_wplaty.insert({"id_wplaty": 0, "id_faktury": 0, "wartosc_wplaty": 0, "waluta": "", "data": "", "kurs": 0, "wartosc_wplaty_pln": 0})

def id_faktury():
    return(db_faktury.all()[-1]['id_faktury'] + 1)

def id_wplaty():
    return(db_wplaty.all()[-1]['id_faktury'] + 1)

def zapisz_fakture(faktura):
    db_faktury.insert(faktura)

def zapisz_wplate(wplata):
    db_wplaty.insert(wplata)
    
def oplac_fakture(id, wplata, wplata_pln, waluta, data, kurs):
    faktura = Query()
    rekord = db_faktury.search(faktura.id_faktury == id)[0]
    status_platnosci = rekord["status_platnosci"]
    print(f"Kwota przed opłatą: {status_platnosci} po przeliczeniu na PLN.")
    status_platnosci = round(status_platnosci - wplata_pln, 2)
    db_faktury.update({"status_platnosci": status_platnosci})
    print(f"Opłacono: {wplata} {waluta}, w przeliczeniu: {wplata_pln} PLN po kursie {kurs} w dniu {data}.")
    print(f"Kwota po opłacie: {status_platnosci} po przeliczeniu na PLN.")
    if rekord["waluta"] == waluta:
        tabela = [["Data faktury", "Data spłaty", "Waluta", "Różnica kursowa"],
                  [rekord["data"], data, waluta, "X"],
                  [rekord["kurs_waluty"], kurs, waluta, rekord["kurs_waluty"] - kurs]]
        print(f"Faktura opłacona w tej samej walucie, różnica kursowa wynosi:")
        print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'))
    
def wyczysc_baze_faktur():
    db_faktury.truncate()
def wyczysc_baze_wplat():
    db_wplaty.truncate()
    
def wyszukaj_fakture(id):
    faktura = Query()
    return db_faktury.search(faktura.id_faktury == id)

def wyszukaj_fakture_nazwa(nazwa):
    faktura = Query()
    return db_faktury.search(faktura.firma == nazwa)

def wszystkie_faktury():
    return db_faktury.all()[1:]

wszystkie_faktury()

#wyczysc_baze_faktur()
#wyczysc_baze_wplat()