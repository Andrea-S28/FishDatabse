import pandas as pd
import random
import string
from PycharmProjects.FishDatabase import Fish as f


def get_common_name(fish_id):
    fish_database_file = pd.read_csv('./Michigan_Fish_20240923.csv')
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
    return fish_common_name


def find_user_exist(user_id):
    users_file = pd.read_csv('Users.csv')
    if user_id in users_file['UserID'].values:
        return True
    return False


def add_user(user_name):
    users_file = pd.read_csv('Users.csv')
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
    users_file = users_file.append(new_user, ignore_index=True)
    # Save the updated DataFrame back to the CSV file
    users_file.to_csv('Users.csv', index=False)

    return user_id

def remove_user(user_id):
    users_file = pd.read_csv('Users.csv')
    users_file = users_file[users_file['UserID'] != user_id]
    users_file.to_csv('Users.csv', index=False)

    return not find_user_exist(user_id)


def find_username(user_id):
    users_file = pd.read_csv('Users.csv')
    if find_user_exist(user_id):
        return users_file[users_file['UserID'] == user_id]['Names'].values[0]
    return 'Could not find user'


def find_user_caught_history(user_id):
    users_file = pd.read_csv('Users.csv')
    if find_user_exist(user_id):
        user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]

        if pd.isnull(user_catches) or user_catches == '':
            return 'No caught fish have been caught yet!'

        all_caught_fish = ''
        for fish_id in user_catches.split(','):
            fish_id = int(fish_id)
            all_caught_fish += f.get_fish(fish_id)
        return all_caught_fish

    return 'Could not find user'


def add_caught_fish(user_id, fish_id):
    if find_user_exist(user_id):
        users_file = pd.read_csv('Users.csv')
        fish_database_file = pd.read_csv('./Michigan_Fish_20240923.csv')
        if fish_id not in fish_database_file['id'].values:
            return f"Fish ID {fish_id} not found."

        user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]
        if pd.isnull(user_catches) or user_catches == '':
            users_file[users_file['UserID'] == user_id]['FishIDs'].values[0] = ""
            user_catches = str(fish_id)
        else:
            user_catches += ',' + str(fish_id)

        users_file.loc[users_file['UserID'] == user_id, 'FishIDs'] = str(user_catches)
        users_file.to_csv('Users.csv', index=False)
    else:
        return "User not found"


