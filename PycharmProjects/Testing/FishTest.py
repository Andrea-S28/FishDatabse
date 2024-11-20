from PycharmProjects.FishDatabase import Fish as f


def test_add_fish_info():
    fish_id = f.add_fish_info("Marlin", "Clownfish", "Marlin is a orange saltwater clownfish with three stripes.")
    assert True == f.find_fish_exist(fish_id)
    f.remove_fish(fish_id)
    print("test_add_fish_info passed successfully!")


def test_remove_fish():
    fish_id = f.add_fish_info("Bruce", "Great White", "Bruce is a massive Great White Shark native to Australia.")
    assert True == f.find_fish_exist(fish_id)
    f.remove_fish(fish_id)
    assert False == f.find_fish_exist(fish_id)
    print("test_remove_fish passed successfully!")


def test_find_fish_exist():
    fish_id = 1
    assert True == f.find_fish_exist(fish_id)
    assert False == f.find_fish_exist(100)
    print("test_find_fish_exist passed successfully")


def test_get_fish():
    fish_desc = f.get_fish(36)
    expected = "Common Name: " + "Spottail Shiner" + '\n' + 'Latin Name: ' + "Notropis hudsonius" + '\n'
    assert fish_desc == expected
    print("test_get_fish passed successfully")


test_add_fish_info()
test_remove_fish()
test_find_fish_exist()
test_get_fish()
