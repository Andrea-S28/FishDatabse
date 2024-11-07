from PycharmProjects.FishDatabase import Fish as f

def test_add_catch():
    fish_id = f.add_fish_info("Marlin", "Clownfish", "Marlin is a orange saltwater clownfish with three stripes.")
    assert True == f.find_fish_exist(fish_id)
    f.remove_fish(fish_id)