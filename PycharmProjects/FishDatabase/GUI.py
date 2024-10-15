import PySimpleGUI as sg
import main as m

layout = [
    [sg.Text("Enter fishID:")],
    [sg.Input(key='-INPUT-')],
    [sg.Image(key="-IMAGE-")],
    [sg.FileBrowse("Choose Image", file_types=(("Image Files", "*.png"),)), sg.Button("Upload Fish")],
    [sg.Button('Ok'), sg.Button('Cancel')],
    [sg.Text(key='-OUTPUT-')]
]

window = sg.Window('Fish Database', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Ok':
        fish_id = int((values["-INPUT-"]))
        fish_description = m.get_fish(fish_id)
        window['-OUTPUT-'].update(fish_description)

    if event == "Upload Fish":
        filename = values["Choose Image"]
        if filename:
            try:
                window['-OUTPUT-'].update(filename)
                # prints file path of image.. this needs to get sent off to Fishial_recognition for processing

                # Process needs to send back FISH ID
                # Fish ID needs to be sent to GetFish Func to return data on uploaded fish
                # OR
                # Process needs to find information on fish and send back fish description

                # save Fish Id to User if User is logged in

                # If no fish found
                # Print Error message
            except Exception as e:
                sg.popup_error(f"Error loading image: {e}")

window.close()