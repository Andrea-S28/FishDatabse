import PySimpleGUI as sg
import Fish as f
import Users as u


current_user_id = ''
current_username = ''

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

def create_create_account_page():
    layout = [
        [sg.Text("Enter your name!")],
        [sg.Input(key='-INPUT-')],
        [sg.Button("Create Account")],
        [sg.Button("go to Log In")],
        [sg.Button("Cancel")],
        [sg.Text(key='-OUTPUT-')]
    ]
    return sg.Window("Create Account", layout)

def create_user_page():
    layout = [
        [sg.Text("Welcome " + current_username )],
        [sg.Text(key='-OUTPUT-')],
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse("Choose Image", file_types=(("Image Files", "*.png"),)), sg.Button("Upload Fish")],
        [sg.Button("Log Out")],
        [sg.Button("Get Caught Fish History")]
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

                if not u.find_user_exist(user_id):
                    log_in['-OUTPUT-'].update("Could not find user. Please try again or create an account")

                else:
                    current_user_id = user_id
                    current_username = u.find_username(user_id)
                    event = 'User'
                    log_in.close()

        # while true -> log in with userID
        # if successful bring to user Page
        # if not, prompt to try again or create account

    # User Page
    if event == 'User':
        user = create_user_page()

        while True:
            event_user_page, values_user = user.read()
            if event_user_page == sg.WIN_CLOSED or event_user_page == "Log Out":
                current_user_id = ''
                current_username = ''
                user.close()
                break



     # Create Account Page
    if event == 'Create Account':
        create_account = create_create_account_page()
        while True:
            event_create_account, values_create_account = create_account.read()
            if event_create_account == sg.WIN_CLOSED or event_create_account == "Cancel":
                create_account.close()
                break

            if event_create_account == "Create Account":
                user_name = values_create_account["-INPUT-"]
                if len(user_name) > 0:
                    # make user
                    user_info = u.add_user(str(user_name))
                    create_account['-OUTPUT-'].update(user_info)
                else:
                    create_account['-OUTPUT-'].update("Please enter a valid name!")

            if event_create_account == "go to Log In":
                event = "Log In"
                create_account.close()
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
                fish_description = f.get_fish(fish_id)
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
