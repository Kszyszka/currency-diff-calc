from sys import path, argv
path.insert(1, "src")

import menu

def main():
    argumenty = argv[1:]
    if "-h" in argumenty or "--help" in argumenty:
        print("Witaj w programie księgowym z funkcją obliczania róznic kursowych - Autor: Krzysztof Hager 52687\n")
        print("Program obsługuje kilka typów argumentów:")
        print("\t'-fF' (fileFaktura) - Gdzie jako kolejny argument przyjmowana jest ścieżka do pliku .csv, z którego zostaną wgrane Faktury.")
        print("\tnp.: python main.py -fF faktury.csv\n")
        print("\t'-fW' (fileWpłata) - Gdzie jako kolejny argument przyjmowana jest ścieżka do pliku .csv, z którego zostaną wgrane Wpłaty do faktur.")
        print("\tnp.: python main.py -fF C:\\Users\\{username}\\faktury.csv\n")
        print("W przypadku złego podania argumentów lub ich braku, zostanie wywołany cały program w wersji interaktywnej.")
        return 1
    if "-fF" in argumenty:
        try:
            plik = argumenty[argumenty.index("-fF") + 1]
        except IndexError:
            print("Nie znaleziono pliku.")
            return 0
        if plik[-3:] == "csv":
            try:
                with open(plik, "r", encoding="UTF-8") as plik:
                    for i in plik.readlines():
                        dane = i.split(',')
                        dane_oczyszczone = [s.strip() for s in dane]
                        dane_oczyszczone[0] = dane_oczyszczone[0].capitalize()
                        dane_oczyszczone[1] = dane_oczyszczone[1].upper()
                        if len(dane_oczyszczone) == 4:
                            menu.faktury.wprowadzenie_faktury_z_pliku(dane_oczyszczone[0], dane_oczyszczone[1], dane_oczyszczone[2], dane_oczyszczone[3])
                        else:
                            print("Nieprawidłowa ilość danych.")
            except FileNotFoundError:
                print("Nie znaleziono pliku.")
                return 0
        else:
            print("Program przyjmuje jedynie pliki .csv")
        return 1
    if "-fW" in argumenty:
        try:
            plik = argumenty[argumenty.index("-fW") + 1]
        except IndexError:
            print("Nie znaleziono pliku.")
            return 0
        if plik[-3:] == "csv":
            try:
                with open(plik, "r", encoding="UTF-8") as plik:
                    for i in plik.readlines():
                        dane = i.split(',')
                        dane_oczyszczone = [s.strip() for s in dane]
                        dane_oczyszczone[2] = dane_oczyszczone[2].upper()
                        if len(dane_oczyszczone) == 4:
                            menu.wplaty.wprowadzenie_wplaty_z_pliku(dane_oczyszczone[0], dane_oczyszczone[1], dane_oczyszczone[2], dane_oczyszczone[3])
                        else:
                            print("Nieprawidłowa ilość danych.")
            except FileNotFoundError:
                print("Nie znaleziono pliku.")
                return 0
        else:
            print("Program przyjmuje jedynie pliki .csv")
        return 1
    menu.menu()
        
    
if __name__ == "__main__":
    main()