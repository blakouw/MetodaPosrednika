import PySimpleGUI as sg

# Funkcja obliczająca punktację dla każdej opcji
def oblicz_punktacje(opcje, kryteria, wagi):
    punktacja = []

    # Stwórz tabelę z wartościami kryteriów dla każdej opcji
    tablica = [[int(y) for y in x.split(',')] for x in opcje.values()]

    # Oblicz sumy ważone dla każdej opcji
    sumy_wazone = [sum([tablica[i][j] * wagi[j] for j in range(len(kryteria))]) for i in range(len(opcje))]

    # Oblicz sumy wag kryteriów
    sumy_wag = [sum([wagi[j] for j in range(len(kryteria))]) for i in range(len(opcje))]

    # Oblicz punktację dla każdej opcji
    for i in range(len(opcje)):
        s = sum([wagi[j] * tablica[i][j] / sumy_wag[i] for j in range(len(kryteria))])
        punktacja.append(s)

    # Znajdź najlepszą opcję
    najlepsza_opcja = list(opcje.keys())[punktacja.index(max(punktacja))]

    # Zwróć najlepszą opcję i jej punktację
    return najlepsza_opcja, max(punktacja)

# Stwórz interfejs użytkownika
layout = [[sg.Text("Wprowadź nazwy opcji rozwiązania:")],
          [sg.Multiline(size=(50, 5), key="-OPCJE-")],
          [sg.Text("Wprowadź nazwy kryteriów:")],
          [sg.Multiline(size=(50, 2), key="-KRYTERIA-")],
          [sg.Text("Wprowadź wartości kryteriów dla każdej opcji:")],
          [sg.Multiline(size=(50, 5), key="-WARTOSCI-")],
          [sg.Button("Oblicz"), sg.Button("Wyjdź")]]

window = sg.Window("Zagadnienie pośrednika", layout)

# Rozpocznij pętlę zdarzeń
while True:
    event, values = window.read()

    # Wyjdź z programu, jeśli naciśnięto przycisk "Wyjdź"
    if event == sg.WIN_CLOSED or event == "Wyjdź":
        break

    # Pobierz wprowadzone wartości i podziel na listy
    opcje = dict(enumerate([x.strip() for x in values["-OPCJE-"].split('\n') if x.strip() != '']))
    kryteria = [x.strip() for x in values["-KRYTERIA-"].split('\n') if x.strip() != '']
    wagi = [1.0] * len(kryteria)
    wartosci = [x.strip() for x in values["-WARTOSCI-"].split('\n') if x.strip() != '']

    # Sprawdź, czy wprowadzone dane są poprawne
    if len(opcje) == 0:
        sg.popup("Wprowadź co najmniej jedną opcję rozwiązania.")
        continue

    if len(kryteria) == 0:
        sg.popup("Wprowadź co najmniej jedno kryterium.")
        continue

    # Sprawdź, czy liczba wprowadzonych wartości kryteriów dla każdej opcji jest zgodna z liczbą kryteriów
    for i in range(len(wartosci)):
        liczba_wartosci = len(wartosci[i].split(','))

        if liczba_wartosci != len(kryteria):
            sg.popup(f"Opcja {i + 1} zawiera niepoprawną liczbę wartości. Wprowadź wartości dla każdego kryterium.")

            # Wyczyść pole z wartościami i przerwij pętlę
            window["-WARTOSCI-"].update("")
            break
    # Oblicz punktację i wyświetl wynik
    najlepsza_opcja, punktacja = oblicz_punktacje(opcje, kryteria, wagi)
    sg.popup(f"Najlepszą opcją jest: {najlepsza_opcja}\n\nPunktacja: {punktacja:.2f}")