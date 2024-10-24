import pandas as pd
import random
import string
import Fish as m


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

    #TODO
    #return f"User {user_name} added successfully with UserID: {user_id}"
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
            all_caught_fish += m.get_fish(fish_id) + '/n'
        return all_caught_fish

    return 'Could not find user'

def add_caught_fish(user_id, fish_id):
    if find_user_exist(user_id):
        pass

    return "User not found"



# def find_user(user_id):
#     users_file = pd.read_csv('Users.csv')
#
#     if user_id not in users_file['UserID'].values:
#         return f"Error: User {user_id} not found in our database."
#
#     user_name = users_file[users_file['UserID'] == user_id]['Names'].values[0]
#     user_login = users_file[users_file['UserID'] == user_id]['UserID'].values[0]
#     user_catches = users_file[users_file['UserID'] == user_id]['FishIDs'].values[0]
#
#     all_fish = []
#     for fish in user_catches.split(','):
#         fish_description = get_common_name(fish.strip())
#         all_fish.append(fish_description)
#
#     user_info = ('Welcome: ' + user_name + '\n' + 'These are Your Catches: ' + '\n')
#     fish_info = '\n'.join(all_fish)
#     return user_info + fish_info


# ____________________ Test ______________________________________________________________
# TODO: add_caught_fish

def test_find_username_success():
    user_id = 'CB363'
    expected_username = 'Carmen Towns'
    returned_username = find_username(user_id)
    assert returned_username == expected_username
    print("test_find_username_success passed successfully!")

def test_find_username_failure():
    user_id = 'Fake_ID'
    expected_username = 'Could not find user'
    returned_username = find_username(user_id)
    assert returned_username == expected_username
    print("test_find_username_failure passed successfully!")

def test_create_user():
    user_id = add_user("Peter Piper")
    assert True == find_user_exist(user_id)
    remove_user(user_id)
    print("test_create_user passed successfully!")

def test_find_user_caught_history_fish_found():
    user_id = 'JW912'
    expected_description = ''
    expected_description += m.get_fish(18) + '/n'
    expected_description += m.get_fish(12) + '/n'

    actual_description = find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_fish_found passed successfully!")

def test_find_user_caught_history_no_fish_found():
    user_id = 'II142'
    expected_description = 'No caught fish have been caught yet!'

    actual_description = find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_no_fish_found passed successfully!")

def test_find_user_caught_history_user_not_found():
    user_id = 'Fake_Id'
    expected_description = 'Could not find user'

    actual_description = find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_user_not_found passed successfully!")

def test_remove_user_user_in_database():
    user_id = add_user("Peter Piper")
    remove_user(user_id)
    assert False == find_user_exist(user_id)
    print("test_remove_user_user_in_database passed successfully!")

def test_remove_user_user_not_in_database():
    user_id = 'Fake_Id'
    remove_user(user_id)
    assert False == find_user_exist(user_id)
    print("test_remove_user_user_not_in_database passed successfully!")


# def test_find_user():
#     print("Testing with user ID 1:")
#     print(find_user("CL149"))  # Expected: Name: John Doe, Catches: Fish123
#
#     print("\nTesting with user ID 2:")
#     print(find_user("BR521"))  # Expected: Name: Jane Smith, Catches: Fish456
#
#     print("\nTesting with user ID that doesn't exist (e.g., 5):")
#     print(find_user("l"))  # Expected: User not found

# test_find_user()



test_create_user()
test_find_username_success()
test_find_username_failure()
test_find_user_caught_history_fish_found()
test_find_user_caught_history_no_fish_found()
test_find_user_caught_history_user_not_found()
test_remove_user_user_in_database()
test_remove_user_user_not_in_database()
