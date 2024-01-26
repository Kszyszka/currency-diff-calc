from tinydb import TinyDB, Query

db_faktury = TinyDB("data/faktury.json")
db_wplaty = TinyDB("data/wplaty.json")

if len(db_faktury.all()) == 0:
    db_faktury.insert({'id_faktury': 0, 'firma': '', 'waluta': '', 'data': '', 'kwota_naleznosci': 0, 'status_platnosci': 0})

def id_faktury():
    return(db_faktury.all()[-1]['id_faktury'] + 1)

def zapisz_fakture(faktura):
    db_faktury.insert(faktura)
    
    
id_faktury()