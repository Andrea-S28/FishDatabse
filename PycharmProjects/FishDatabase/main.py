import textwrap
import pandas as pd
import random
import string


def add_catch(fish_name, fish_latin_name, fish_details, fish_image = None):
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
    return f"{fish_name} successfully added to your catches."


def get_fish(fish_id):
    df = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_common_name = df[df['id'] == fish_id]['CommonName'].values[0]
    fish_latin_name = df[df['id'] == fish_id]['LatinName'].values[0]
    fish_details = df[df['id'] == fish_id]['Narrative'].values[0]

    fish_desc = ('Common Name: ' + fish_common_name + '\n' + 'Latin Name: ' + fish_latin_name + '\n')

    new_text = textwrap.fill(fish_details, 60)
    fish_desc += 'Description: ' + new_text

    return fish_desc


def test_add_catch():
    print("Testing with fish Marlin:")
    add_catch("Marlin", "Clownfish", "Marlin is a orange saltwater clownfish with three stripes.")


#test_add_catch()