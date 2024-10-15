import textwrap
import pandas as pd


def get_fish(fish_id):
    df = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_common_name = df[df['id'] == fish_id]['CommonName'].values[0]
    fish_latin_name = df[df['id'] == fish_id]['LatinName'].values[0]
    fish_details = df[df['id'] == fish_id]['Narrative'].values[0]

    fish_desc = ('Common Name: ' + fish_common_name + '\n' + 'Latin Name: ' + fish_latin_name + '\n')

    new_text = textwrap.fill(fish_details, 60)
    fish_desc += 'Description: ' + new_text

    return fish_desc
