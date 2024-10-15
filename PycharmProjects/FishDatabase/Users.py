import pandas as pd
import random
import string


def get_common_name(fish_id):
    df = pd.read_csv('./Michigan_Fish_20240923.csv')

    # Ensure fish_id is an integer
    try:
        fish_id = int(fish_id)
    except ValueError:
        return f"Invalid fish ID: {fish_id}"

    # Check if the fish ID exists
    if fish_id not in df['id'].values:
        return f"Fish ID {fish_id} not found."

    # Get the common name
    try:
        fish_common_name = df[df['id'] == fish_id]['CommonName'].values[0]
        return fish_common_name
    except IndexError:
        return f"Fish ID {fish_id} not found."


def add_user(user_name):
    df = pd.read_csv('Users.csv')

    id_letter_key = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
    id_number_key = ''.join(random.choice(string.digits) for i in range(3))

    user_id = id_letter_key + id_number_key

    # Add the new user with an empty FishIDs field
    new_user = {
        'UserID': user_id,
        'Names': user_name,
        'FishIDs': ''  # Initially, no fish catches for the new user
    }

    # Append the new user to the DataFrame
    df = df.append(new_user, ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv('Users.csv', index=False)

    return f"User {user_name} added successfully with UserID: {user_id}"


def find_user(user_id):
    df = pd.read_csv('Users.csv')
    user_name = df[df['UserID'] == user_id]['Names'].values[0]
    user_login = df[df['UserID'] == user_id]['UserID'].values[0]
    user_catches = df[df['UserID'] == user_id]['FishIDs'].values[0]

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
    print(find_user("JW912"))  # Expected: User not found


test_find_user()


def test_create_user():
    print("Testing with user Peter Piper:")
    add_user("Peter Piper:")


#test_create_user()
