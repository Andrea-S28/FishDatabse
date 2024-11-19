import pandas as pd
import random
import string
from PycharmProjects.FishDatabase import Fish as f
import os


def get_common_name(fish_id):
    fish_database_file = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
    fish_database_file = pd.read_csv(fish_database_file)
    # Ensures fish_id is an integer
    try:
        fish_id = int(fish_id)
    except ValueError:
        return f"Invalid fish ID: {fish_id}, needs to be a number value with no spaces"

    # Blocks any invalid entries from proceeding
    if fish_id not in fish_database_file['id'].values:
        return f"Fish ID {fish_id} not found."

    # Get the common name of the selected fish
    fish_common_name = fish_database_file[fish_database_file['id'] == fish_id]['CommonName'].values[0]
    return str(fish_id)+": " + fish_common_name + '\n'


def find_user_exist(user_id):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    if user_id in users_file['UserID'].values:
        return True
    return False


def add_user(user_name):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    # Randomizes the values of the id
    id_letter_key = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
    id_number_key = ''.join(random.choice(string.digits) for i in range(3))
    user_id = id_letter_key + id_number_key

    # Adds the new users values, fish ids starting as blank
    new_user = {
        'UserID': user_id,
        'Names': user_name,
        'FishIDs': ""
    }

    # Add the new user to the end of the Users file
    users_file = users_file._append(new_user, ignore_index=True)
    # Save the updated DataFrame back to the CSV file
    users_file.to_csv(user_path, index=False)

    return user_id

def remove_user(user_id):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    users_file = users_file[users_file['UserID'] != user_id]
    users_file.to_csv(user_path, index=False)

    return not find_user_exist(user_id)


def find_username(user_id):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    if find_user_exist(user_id):
        return users_file[users_file['UserID'] == user_id]['Names'].values[0]
    return 'Could not find user'


def find_user_caught_history(user_id):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    if find_user_exist(user_id):
        user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]

        if pd.isnull(user_catches) or user_catches == '':
            return 'No caught fish have been caught yet!'

        all_caught_fish = ''
        for fish_id in user_catches.split(','):
            fish_id = int(fish_id)
            all_caught_fish += get_common_name(fish_id)
        return all_caught_fish

    return 'Could not find user'


def add_caught_fish(user_id, fish_id):
    if find_user_exist(user_id):
        user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
        users_file = pd.read_csv(user_path)

        fish_path = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
        fish_file = pd.read_csv(fish_path)

        if fish_id not in fish_file['id'].values:
            return f"Fish ID {fish_id} not found."

        user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]
        if pd.isnull(user_catches) or user_catches == '':
            users_file[users_file['UserID'] == user_id]['FishIDs'].values[0] = ""
            user_catches = str(fish_id)
        else:
            user_catches += ',' + str(fish_id)

        users_file.loc[users_file['UserID'] == user_id, 'FishIDs'] = str(user_catches)
        users_file.to_csv(user_path, index=False)
        return f"Successfully added the fishID: {fish_id} to your history!"
    else:
        return "User not found"


def remove_catch(user_id, fish_id):
    user_path = os.path.join(os.path.dirname(__file__), 'Users.csv')
    users_file = pd.read_csv(user_path)
    user_index = users_file[users_file['UserID'] == user_id].index[0]
    current_fish_ids = users_file.at[user_index, 'FishIDs']

    if pd.isnull(current_fish_ids) or current_fish_ids == '':
        return 'You have no fish in your caught history yet!'
    fish_ids_list = current_fish_ids.split(',')
    if str(fish_id) in fish_ids_list:
        fish_ids_list.remove(str(fish_id))

        updated_fish_ids = ','.join(fish_ids_list) if fish_ids_list else ''
        users_file.loc[users_file['UserID'] == user_id, 'FishIDs'] = updated_fish_ids
        users_file.to_csv(user_path, index=False)
        return f'Successfully removed FishID:{fish_id} from your history!'
    return f'Could not find FishID:{fish_id} in your history.'
