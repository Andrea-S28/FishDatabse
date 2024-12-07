import PySimpleGUI as sg
import Fish as f
import Users as u
import prediction as p


current_user_id = ''
"""Used to track which user is active"""
current_username = ''
"""Stores username of currently logged-in user"""
current_fish_id = ''
"""Stores the ID of the fish currently being identified"""


def create_welcome_page():
    """
    create_welcome_page()
    This function is used to create the layout for the welcome page.
    It initializes the buttons to allow the users to click into the other pages.
    """
    layout = [
        [sg.Text("Welcome to Fish Database!")],
        [sg.Button("Log In")],
        [sg.Button("Create Account")],
        [sg.Button("Guest")]
    ]
    return sg.Window("Welcome", layout)


def create_guest_page():
    """
    create_guest_page()
    This function is used to create the guest page. It creates the layout for the guest page.
    """
    layout = [
        [sg.Text("Welcome to the guest page! Select an image of a fish to upload.")],
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse("Choose Image", file_types=(("Image Files", "*.png;*.jpeg;*.jpg"),)), sg.Button("Upload Fish")],
        [sg.Button('Cancel')],
        [sg.Text(key='-OUTPUT-')]
    ]
    return sg.Window("Guest Page", layout)


def create_log_in_page():
    """
    create_log_in_page()
    This function creates the login page.
    It creates the layout as well as buttons to click into the user page after a successful login.
    """
    layout = [
        [sg.Text("Enter UserID")],
        [sg.Input(key='-INPUT-')],
        [sg.Button("Log In")],
        [sg.Button("Cancel")],
        [sg.Text(key='-OUTPUT-')]
    ]
    return sg.Window("Log In", layout)


def create_create_account_page():
    """
    create_create_account_page()
    This function creates the create account page.
    It sets up the layout as well as initializes the button to allow the user to click into the login page.
    """
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
    """
    create_user_page()
    This function is used to create the user page.
    It sets up the layout of the page as well as initializes the buttons the user will use on this page.
    """
    layout = [
        [sg.Text("Welcome " + current_username)],
        [sg.Text("Enter fishID to remove from history:")],
        [sg.Input(key='-INPUT-')],
        [sg.Text(key='-OUTPUT-')],
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse("Choose Image", file_types=(("Image Files", "*.png;*.jpeg;*.jpg"),)), sg.Button("Upload Fish")],
        [sg.Button("Log Out")],
        [sg.Button("Get Caught History")],
        [sg.Button("Add Catch to History")],
        [sg.Button("Remove Catch from History")],
    ]
    return sg.Window("User", layout)


welcome = create_welcome_page()
"""the window object for the welcome page"""

while True:
    event, values = welcome.read()

    if event == sg.WIN_CLOSED:
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

    # User Page
    if event == 'User':
        user = create_user_page()

        while True:
            event_user_page, values_user = user.read()
            if event_user_page == sg.WIN_CLOSED or event_user_page == "Log Out":
                current_user_id = ''
                current_username = ''
                current_fish_id = ''
                user.close()
                break

            # Upload Fish
            if event_user_page == "Upload Fish" or event_user_page == "Add Catch to History":
                filename = values_user["Choose Image"]
                if filename:
                    try:
                        predicted_label = p.prediction(filename)

                        user['-OUTPUT-'].update(predicted_label)
                        current_fish_id = int(predicted_label)
                        fish_description = f.get_fish(current_fish_id)
                        user['-OUTPUT-'].update(fish_description)
                    except Exception as e:
                        sg.popup_error(f"Error loading image: {e}")

            # Get Caught Fish History
            if event_user_page == "Get Caught History":
                caught_history = u.find_user_caught_history(current_user_id)
                user['-OUTPUT-'].update(caught_history)

            # add catch to caught history
            if event_user_page == "Add Catch to History":
                added = u.add_caught_fish(current_user_id, current_fish_id)
                user['-OUTPUT-'].update(added)

            # remove catch from caught history
            if event_user_page == "Remove Catch from History":
                current_fish_id = values_user["-INPUT-"]
                removed = u.remove_catch(current_user_id, current_fish_id)
                user['-OUTPUT-'].update(removed)

    # Guest Page
    if event == "Guest":
        guest = create_guest_page()
        while True:
            event_guest_page, guest_values = guest.read()
            if event_guest_page == sg.WIN_CLOSED or event_guest_page == "Cancel":
                guest.close()
                break

            # Get Fish by Photo
            if event_guest_page == "Upload Fish":
                filename = guest_values["Choose Image"]
                if filename:
                    try:
                        predicted_label = p.prediction(filename)
                        guest['-OUTPUT-'].update(predicted_label)
                        fish_id = int(predicted_label)
                        fish_description = f.get_fish(fish_id)
                        guest['-OUTPUT-'].update(fish_description)
                    except Exception as e:
                        sg.popup_error(f"Error loading image: {e}")

welcome.close()
