import PySimpleGUI as sg
import main as m
import Users as user


def create_welcome_page():
    layout = [
        [sg.Text("Welcome to Fish Database!")],
        [sg.Button("Log In")],
        [sg.Button("Create Account")],
        [sg.Button("Guest")]
    ]
    return sg.Window("Welcome", layout)


def create_guest_page():
    layout = [
        [sg.Text("Enter fishID:")],
        [sg.Input(key='-INPUT-')],
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse("Choose Image", file_types=(("Image Files", "*.png"),)), sg.Button("Upload Fish")],
        [sg.Button('Ok'), sg.Button('Cancel')],
        [sg.Text(key='-OUTPUT-')]
    ]
    return sg.Window("Guest Page", layout)


def create_log_in_page():
    layout = [
        [sg.Text("Enter UserID")],
        [sg.Input(key='-INPUT-')],
        [sg.Button("Log In")],
        [sg.Button("Cancel")],
        [sg.Text(key='-OUTPUT-')]
    ]
    return sg.Window("Log In", layout)


def create_user_page():
    layout = [
        [sg.Text("Welcome User")],
        [sg.Button("Cancel")]
    ]
    return sg.Window("User", layout)


welcome = create_welcome_page()

while True:
    event, values = welcome.read()

    if event == sg.WIN_CLOSED:
        break

    # Log In Page
    if event == "Log In":
        log_in = create_log_in_page()
        while True:
            event_log_in_page, log_in_values = log_in.read()
            if event_log_in_page == sg.WIN_CLOSED or event_log_in_page == "Cancel":
                log_in.close()
                break

            if event_log_in_page == "Log In":
                user_id = log_in_values["-INPUT-"]

                try:
                    user_info = user.find_user(user_id)
                    event = 'User'
                    log_in.close()

                except IndexError as e:
                    log_in['-OUTPUT-'].update("Could not find user. Please try again or create an account")

        # while true -> log in with userID
        # if successful bring to user Page
        # if not, prompt to try again or create account

    # User Page
    if event == 'User':
        user = create_user_page()
        while True:
            event_user_page, values_user = user.read()
            if event_user_page == sg.WIN_CLOSED or event_user_page == "Cancel":
                user.close()
                break

    # Guest Page
    if event == "Guest":
        guest = create_guest_page()
        while True:
            event_guest_page, guest_values = guest.read()
            if event_guest_page == sg.WIN_CLOSED or event_guest_page == "Cancel":
                guest.close()
                break

            # Get Fish by Fish ID
            elif event_guest_page == 'Ok':
                fish_id = int((guest_values["-INPUT-"]))
                fish_description = m.get_fish(fish_id)
                guest['-OUTPUT-'].update(fish_description)

            # Get Fish by Photo
            elif event_guest_page == "Upload Fish":
                filename = guest_values["Choose Image"]
                if filename:
                    try:
                        guest['-OUTPUT-'].update(filename)
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

welcome.close()
