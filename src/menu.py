'''Moduł służący do interaktywnej obsługi programu.'''
from os import system
import baza
import faktury
import waluty
import wplaty

# Cały moduł działa na uruchamianiu własnych menu w pętlach
# Jest tak, aby osoba działająca np. ciągle w zakresie faktur
# Nie musiała ciągle ich wybierać w menu, a automatycznie do niego wracała

# Program w zależności od wyboru w menu wywołuje pojedynczą funkcję z końcowego modułu
# Jest to zrobione w ramach czytelności i ułatwienia ewentualnych modyfikacji
def zarzadzanie_fakturami():
    '''Interaktywne zarządzanie fakturami.'''
    system('cls')
    system('clear')
    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Dodaj nową Fakturę.", faktury.wprowadzenie_faktury],
             '2': ["2. Wyszukaj Fakturę po ID.", faktury.wyszukaj_fakture_po_id],
             '3': ["3. Wyszukaj Fakturę po nazwie firmy.", faktury.wyszukaj_fakture_po_nazwie],
             '4': ["4. Wypisz wszystkie faktury.", faktury.wypisz_wszystkie],
             '5': ["5. Sprawdź status płatności Faktury po ID.", faktury.status_platnosci_po_id],
             'back': ["'Back' - Cofnij do poprzedniego menu.", menu],
             'quit': ["Program można opuścić przez 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}

    while True:
        print("ZARZĄDZANIE FAKTURAMI")
        for item in opcje.items():
            print(item[1][0])

        user_input = input("\nWybierz opcję 1, 2, 3, 4, 5: ").strip().lower()
        system('cls')
        system('clear')
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')

def zarzadzanie_wplatami():
    '''Interaktywne zarządzanie wpłatami.'''
    system('cls')
    system('clear')

    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Dodaj nową wpłatę.", wplaty.wprowadzenie_wplaty],
             '2': ["2. Wyszukaj wpłaty po ID Wpłaty.", wplaty.wyszukaj_wplate_po_id],
             '3': ["3. Wyszukaj wpłatę po ID Faktury.", wplaty.wyszukaj_wplate_po_id_faktury],
             '4': ["4. Usuń wpłatę.", wplaty.usun_wplate],
             'back': ["'Back' - Cofnij do poprzedniego menu.", menu],
             'quit': ["Program można opuścić przez 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}

    while True:
        print("ZARZĄDZANIE WPŁATAMI")

        for item in opcje.items():
            print(item[1][0])

        user_input = input("\nWybierz opcję 1, 2, 3, 4: ").strip().lower()
        system('cls')
        system('clear')
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')

def roznice_kursowe():
    '''Interaktywna obsługa różnic kursowych.'''
    system('cls')
    system('clear')

    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Oblicz różnicę kursową dwóch dowolnych dat.", waluty.roznica_kursowa],
             '2': ["2. Oblicz różnicę kursową pomiędzy Fakturą, a wpłatą.", wplaty.roznice_kursowe],
             '3': ["3. Sprawdź kurs podanej waluty konkretnego dnia.", waluty.konkretna_data],
             'back': ["'Back' - Cofnij do poprzedniego menu.", menu],
             'quit': ["Program można opuścić przez 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}

    while True:
        print("RÓŻNICE KURSOWE")

        for item in opcje.items():
            print(item[1][0])

        user_input = input("\nWybierz opcję 1, 2, 3: ").strip().lower()
        system('cls')
        system('clear')
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')

def zarzadzanie_bazami():
    '''Interaktywna obsługa baz danych.'''
    system('cls')
    system('clear')

    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Wyczyść bazę faktur.", baza.wyczysc_baze_faktur],
             '2': ["2. Wyczyść bazę wpłat.", baza.wyczysc_baze_wplat],
             'back': ["'Back' - Cofnij do poprzedniego menu.", menu],
             'quit': ["Program można opuścić przez 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}

    while True:
        print("ZARZĄDZANIE BAZAMI DANYCH")

        for item in opcje.items():
            print(item[1][0])

        user_input = input("\nWybierz opcję 1, 2: ").strip().lower()
        system('cls')
        system('clear')
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')

def menu():
    '''Funkcja obsługująca główne menu użytkownika.'''
    opcje = {'0': ["\nMożliwe funkcje:", ""],
             '1': ["1. Zarządzaj Fakturami (dodaj, wyszukaj, status).", zarzadzanie_fakturami],
             '2': ["2. Zarządzaj Wpłatami (dodaj, wyszukaj, cofnij).", zarzadzanie_wplatami],
             '3': ["3. Sprawdź różnice kursowe pomiędzy dowolnymi datami.", roznice_kursowe],
             '4': ["4. Zarządzaj Bazą faktur lub wpłat.", zarzadzanie_bazami],
             'quit': ["Program można opuścić przez 'CTRL + C' lub poprzez wpisanie 'Quit'.", quit]}

    while True:
        system('cls')
        system('clear')
        print("Witaj w programie księgowym z funkcją obliczania róznic kursowych")
        print("Autor: Krzysztof Hager 52687'")

        for item in opcje.items():
            print(item[1][0])

        user_input = input("\nWybierz opcję 1, 2, 3, 4: ").strip().lower()
        try:
            opcje[user_input][1]()
        except KeyError:
            print('Wybrana błędna opcja.')
        input()
