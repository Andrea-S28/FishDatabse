from PycharmProjects.FishDatabase import Fish as fish
from PycharmProjects.FishDatabase import Users as user

def test_find_username_success():
    user_id = 'CB363'
    expected_username = 'Carmen Towns'
    returned_username = user.find_username(user_id)
    assert returned_username == expected_username
    print("test_find_username_success passed successfully!")

def test_find_username_failure():
    user_id = 'Fake_ID'
    expected_username = 'Could not find user'
    returned_username = user.find_username(user_id)
    assert returned_username == expected_username
    print("test_find_username_failure passed successfully!")

def test_create_user():
    user_id = user.add_user("Peter Piper")
    assert True == user.find_user_exist(user_id)
    user.remove_user(user_id)
    print("test_create_user passed successfully!")

def test_find_user_caught_history_fish_found():
    user_id = 'JW912'
    expected_description = ''
    expected_description += fish.get_fish(18)
    expected_description += fish.get_fish(12)

    actual_description = user.find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_fish_found passed successfully!")

def test_find_user_caught_history_no_fish_found():
    user_id = 'II142'
    expected_description = 'No caught fish have been caught yet!'

    actual_description = user.find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_no_fish_found passed successfully!")

def test_find_user_caught_history_user_not_found():
    user_id = 'Fake_Id'
    expected_description = 'Could not find user'

    actual_description = user.find_user_caught_history(user_id)

    assert expected_description == actual_description
    print("test_find_user_caught_history_user_not_found passed successfully!")

def test_remove_user_user_in_database():
    user_id = user.add_user("Peter Piper")
    user.remove_user(user_id)
    assert False == user.find_user_exist(user_id)
    print("test_remove_user_user_in_database passed successfully!")

def test_remove_user_user_not_in_database():
    user_id = 'Fake_Id'
    user.remove_user(user_id)
    assert False == user.find_user_exist(user_id)
    print("test_remove_user_user_not_in_database passed successfully!")


def test_add_catch_singular():
    user_id = "II142"
    fish_id = 18
    user.add_caught_fish(user_id, fish_id)
    expected = fish.get_fish(18)
    actual = user.find_user_caught_history(user_id)

    assert actual == expected

def test_add_catch_multiple():
    user_id = "CL149"
    #fish ids for CL149 "5,1,23,4"
    expected = fish.get_fish(5) + fish.get_fish(1) + fish.get_fish(23) + fish.get_fish(4)
    actual = user.find_user_caught_history(user_id)
    assert actual == expected
    user.add_caught_fish(user_id, 33)
    assert actual != expected
    expected += fish.get_fish(33)
    assert actual == expected


