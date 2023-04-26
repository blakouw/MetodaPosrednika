import PySimpleGUI as sg
import numpy as np

# Defining GUI layout
sg.theme('DefaultNoMoreNagging')  # set the color scheme of the GUI
layout = [
    [sg.Text('Dodaj magazyn')],
    [sg.Text('Magazyn:'), sg.InputText(key='magazyn'), sg.Button('Dodaj')],
    [sg.Text('Dodaj dostawcę')],
    [sg.Text('Dostawca:'), sg.InputText(key='dostawca'), sg.Button('Dodaj')],
    [sg.Text('Dodaj koszt')],
    [sg.Text('Magazyn:'), sg.InputCombo([], key='magazyn_koszt'), sg.Text('Dostawca:'),
     sg.InputCombo([], key='dostawca_koszt'), sg.Text('Koszt:'), sg.InputText(key='koszt'), sg.Button('Dodaj')],
    [sg.Text('Tabela kosztów')],
    [sg.Table(values=[], headings=['Magazyn', 'Dostawca', 'Koszt'], key='tabela_kosztow')],
    [sg.Button('Oblicz'), sg.Button('Wyjście')],
    [sg.Text('Tabela zysków jednostkowych')],
    [sg.Table(values=[], headings=['Magazyn', 'Dostawca', 'Zysk'], key='tabela_zyskow')],
    [sg.Text('Tabela optymalnych przewozów')],
    [sg.Table(values=[], headings=['Magazyn', 'Dostawca', 'Przepływ'], key='tabela_przeplywow')],
    [sg.Text('Koszt całkowity: '), sg.Text(key='koszt_calkowity')],
    [sg.Text('Przychód całkowity: '), sg.Text(key='przychod_calkowity')],
    [sg.Text('Zysk pośrednika: '), sg.Text(key='zysk_posrednika')]
]

# Defining variables
magazyny = []
dostawcy = []
koszty = []
zyski = np.array([])
przeplywy = np.array([])

# Create the GUI window
window = sg.Window('Zagadnienie pośrednika', layout)

# Main event loop
while True:
    event, values = window.read()
    if event == 'Dodaj':
        if values['magazyn']:
            magazyny.append(values['magazyn'])
            window['magazyn_koszt'].update(values=magazyny)
            window['magazyn'].update('')
        elif values['dostawca']:
            dostawcy.append(values['dostawca'])
            window['dostawca_koszt'].update(values=dostawcy)
            window['dostawca'].update('')
        elif values['koszt']:
            koszty.append([values['magazyn_koszt'], values['dostawca_koszt'], float(values['koszt'])])
            window['tabela_kosztow'].update(values=koszty)
            window['magazyn_koszt'].update('')
        elif event == 'Oblicz':
            if not magazyny or not dostawcy or not koszty:
                sg.popup('Dodaj magazyny, dostawców oraz koszty')
            continue

            # Creating the cost matrix
            cost_matrix = np.zeros((len(magazyny), len(dostawcy)))
            for koszt in koszty:
                i = magazyny.index(koszt[0])
                j = dostawcy.index(koszt[1])
                cost_matrix[i][j] = koszt[2]

            # Solving the transportation problem
            supply = [1] * len(magazyny)
            demand = [1] * len(dostawcy)
            _, przeplywy, zyski = scipy.optimize.linear_sum_assignment(cost_matrix)

            # Updating tables
            tabela_zyskow = []
            tabela_przeplywow = []
            for i in range(len(magazyny)):
                for j in range(len(dostawcy)):
                    if przeplywy[i] == j:
                        tabela_przeplywow.append([magazyny[i], dostawcy[j], 1])
                        tabela_zyskow.append([magazyny[i], dostawcy[j], koszty[i * len(dostawcy) + j][2]])
                    else:
                        tabela_przeplywow.append([magazyny[i], dostawcy[j], 0])
                        tabela_zyskow.append([magazyny[i], dostawcy[j], 0])

            koszt_calkowity = sum([koszt[2] for koszt in koszty])
            przychod_calkowity = sum(zyski)
            zysk_posrednika = przychod_calkowity - koszt_calkowity

            window['tabela_zyskow'].update(values=tabela_zyskow)
            window['tabela_przeplywow'].update(values=tabela_przeplywow)
            window['koszt_calkowity'].update(koszt_calkowity)
            window['przychod_calkowity'].update(przychod_calkowity)
            window['zysk_posrednika'].update(zysk_posrednika)

        elif event in (sg.WIN_CLOSED, 'Wyjście'):
            break