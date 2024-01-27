from sys import path
from os import system
path.insert(1, "src")

import baza, faktury, waluty, wplaty

def zarzadzanie_fakturami():
    system('cls')
    system('clear')
    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Dodaj nową Fakturę.", faktury.wprowadzenie_faktury],
             '2': ["2. Wyszukaj Fakturę po ID.", faktury.wyszukaj_fakture_po_id],
             '3': ["3. Wyszukaj Fakturę po nazwie firmy.", faktury.wyszukaj_fakture_po_nazwie],
             '4': ["4. Wypisz wszystkie faktury.", faktury.wypisz_wszystkie],
             '5': ["5. Sprawdź status płatności Faktury po ID.", faktury.status_platnosci_po_id],
             'back': ["'Back' - Cofnij do poprzedniego menu.", main],
             'quit': ["Program można opuścić kombinacją 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}
    
    while True:
        print("\nZARZĄDZANIE FAKTURAMI")
        
        for key in opcje:
            print(opcje[key][0])
        
        user_input = input("\nWybierz opcję 1, 2, 3, 4, 5: ").strip().lower()
        system('cls')
        system('clear')
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')
        

def zarzadzanie_wplatami():
    system('cls')
    system('clear')
    print("\nZARZĄDZANIE WPŁATAMI\n")
    
    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Dodaj nową wpłatę.", ],
             '2': ["2. Wyszukaj wpłaty po ID Faktury.", ],
             '3': ["3. Wyszukaj wpłatę.", ],
             '4': ["4. Usuń wpłatę.", ],
             'back': ["'Back' - Cofnij do poprzedniego menu.", main],
             'quit': ["Program można opuścić kombinacją 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}
    
    for key in opcje:
            print(opcje[key][0])
        
    user_input = input("\nWybierz opcję 1, 2, 3, 4, 5: ").strip().lower()
    try:
        opcje[user_input][1]()
    except KeyError:
        print('Wybrana błędna opcja.')
    
def roznice_kursowe():
    system('cls')
    system('clear')
    print("\nRÓŻNICE KURSOWE\n")
    
def zarzadzanie_bazami():
    system('cls')
    system('clear')
    print("\nZARZĄDZANIE BAZAMI DANYCH\n")

def main():    
    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Zarządzaj Fakturami (dodaj nową, wyszukaj aktualne, sprawdź status).", zarzadzanie_fakturami],
             '2': ["2. Zarządzaj Wpłatami (dodaj nową, wyszukaj wpłaty faktury, cofnij wpłatę).", zarzadzanie_wplatami],
             '3': ["3. Sprawdź różnice kursowe pomiędzy dowolnymi datami.", roznice_kursowe],
             '4': ["4. Zarządzaj Bazą faktur lub wpłat.", zarzadzanie_bazami],
             'quit': ["Program można opuścić kombinacją 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}
    
    while True:
        system('cls')
        system('clear')
        print('Witaj w programie księgowym z funkcją obliczania róznic kursowych - Autor: Krzysztof Hager 52687')
        
        for key in opcje:
            print(opcje[key][0])

        user_input = input("\nWybierz opcję 1, 2, 3, 4: ").strip().lower()
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')
            
        
    
if __name__ == "__main__":
    main()