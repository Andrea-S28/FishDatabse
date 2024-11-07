import textwrap
import pandas as pd
import random
import string


def add_fish_info(fish_name, fish_latin_name, fish_details, fish_image = None):
    fish_file = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_id = ''.join(random.choice(string.digits) for i in range(3))

    new_fish = {
        'id': fish_id,
        'CommonName': fish_name,
        'LatinName': fish_latin_name,
        'Narrative': fish_details,
        'ImageURL': fish_image
    }

    fish_file = fish_file.append(new_fish, ignore_index=True)
    fish_file.to_csv('./Michigan_Fish_20240923.csv', index=False)
    #return f"{fish_name} successfully added to your catches."
    return int(fish_id)


def get_fish(fish_id):
    df = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_common_name = df[df['id'] == fish_id]['CommonName'].values[0]
    fish_latin_name = df[df['id'] == fish_id]['LatinName'].values[0]
    fish_details = df[df['id'] == fish_id]['Narrative'].values[0]

    fish_desc = ('Common Name: ' + fish_common_name + '\n' + 'Latin Name: ' + fish_latin_name + '\n')

    #new_text = textwrap.fill(fish_details, 60)
    #fish_desc += 'Description: ' + new_text

    return fish_desc

def find_fish_exist(fish_id):
    fish_dataset = pd.read_csv('./Michigan_Fish_20240923.csv')
    if fish_id in fish_dataset['id'].values:
        return True
    return False


def remove_fish(fish_id):
    fish_dataset = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_dataset = fish_dataset[fish_dataset['id'] != fish_id]
    fish_dataset.to_csv('./Michigan_Fish_20240923.csv', index=False)

    return not find_fish_exist(fish_id)
