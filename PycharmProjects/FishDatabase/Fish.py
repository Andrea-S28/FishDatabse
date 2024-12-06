import pandas as pd
import random
import string
import os

#
# add_fish_info()
# This function takes in a fish name, a fish’s Latin name, fish details, and an image (optional).
# Given the parameters of the function, it will then add the details to the fish database.
# Upon adding the fish to the fish.csv file, the function will then
# return the fish id that was made for that tuple entry.
#


def add_fish_info(fish_name, fish_latin_name, fish_details, fish_image=''):
    fish_path = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
    fish_file = pd.read_csv(fish_path)
    fish_id = ''.join(random.choice(string.digits) for i in range(3))

    new_fish = {
        'id': fish_id,
        'CommonName': fish_name,
        'LatinName': fish_latin_name,
        'Narrative': fish_details,
        'ImageURL': fish_image
    }

    fish_file = fish_file._append(new_fish, ignore_index=True)
    fish_file.to_csv(fish_path, index=False)
    return int(fish_id)


#
# get_fish()
# This function takes in a fish id as a parameter. This function will then query the database for that fish.
# Upon finding the corresponding fish, this function will
# return a description of the fish containing the fish's common name and latin name
#

def get_fish(fish_id):
    fish_path = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
    fish_file = pd.read_csv(fish_path)
    fish_common_name = fish_file[fish_file['id'] == fish_id]['CommonName'].values[0]
    fish_latin_name = fish_file[fish_file['id'] == fish_id]['LatinName'].values[0]

    fish_desc = ('Common Name: ' + fish_common_name + '\n' + 'Latin Name: ' + fish_latin_name + '\n')

    return fish_desc

#
# find_fish_exist()
# This function takes in a fish id. It will then query the fish database.
# If the function successfully finds the fish in the fish.csv file, then it will return true.
# If the id does not exist in the database, then the function returns false.
#


def find_fish_exist(fish_id):
    fish_path = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
    fish_file = pd.read_csv(fish_path)
    if fish_id in fish_file['id'].values:
        return True
    return False

#
# remove_fish()
#   find_fish_exist()
# This function takes in a fish ID as a parameter.
# It will then update the fish database to remove the tuple corresponding to that ID.
# This function calls find_fish_exist() with the same given id to check whether the fish was successfully removed
# from the database or not.
#


def remove_fish(fish_id):
    fish_path = os.path.join(os.path.dirname(__file__), 'Michigan_Fish_20240923.csv')
    fish_file = pd.read_csv(fish_path)
    fish_file = fish_file[fish_file['id'] != fish_id]
    fish_file.to_csv(fish_path, index=False)

    return not find_fish_exist(fish_id)
