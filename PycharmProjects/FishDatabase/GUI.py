import PySimpleGUI as sg
import main as m

layout = [
    [sg.Text("Enter your name:")],
    [sg.Input(key='-INPUT-')],
    [sg.Button('Ok'), sg.Button('Cancel')],
    [sg.Text(key='-OUTPUT-')]
]

window = sg.Window('Updating Text', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Ok':
        fish_id = int((values["-INPUT-"]))
        fish_description = m.get_fish(fish_id)
        window['-OUTPUT-'].update(fish_description)

window.close()