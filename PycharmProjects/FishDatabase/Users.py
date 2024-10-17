import pandas as pd
import random
import string


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
        'FishIDs': ''
    }

    # Add the new user to the end of the Users file
    users_file = users_file.append(new_user, ignore_index=True)
    # Save the updated DataFrame back to the CSV file
    users_file.to_csv('Users.csv', index=False)

    return f"User {user_name} added successfully with UserID: {user_id}"


def find_user(user_id):
    users_file = pd.read_csv('Users.csv')

    if user_id not in users_file['UserID'].values:
        return f"Error: User {user_id} not found in our database."

    user_name = users_file[users_file['UserID'] == user_id]['Names'].values[0]
    user_login = users_file[users_file['UserID'] == user_id]['UserID'].values[0]
    user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]

    all_fish = []
    for fish in user_catches.split(','):
        fish_description = get_common_name(fish.strip())
        all_fish.append(fish_description)

    user_info = ('Welcome: ' + user_name + '\n' + 'These are Your Catches: ' + '\n')
    fish_info = '\n'.join(all_fish)
    return user_info + fish_info


def test_find_user():
    print("Testing with user ID 1:")
    print(find_user("CL149"))  # Expected: Name: John Doe, Catches: Fish123

    print("\nTesting with user ID 2:")
    print(find_user("BR521"))  # Expected: Name: Jane Smith, Catches: Fish456

    print("\nTesting with user ID that doesn't exist (e.g., 5):")
    print(find_user("l"))  # Expected: User not found


test_find_user()


#def test_create_user():
    #print("Testing with user Peter Piper:")
    #add_user("Peter Piper:")


#test_create_user()