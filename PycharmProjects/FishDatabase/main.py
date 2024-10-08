import pandas as pd

def get_fish(fish_id):
    df = pd.read_csv('./Michigan_Fish_20240923.csv')
    fish_common_name = df[df['id'] == fish_id]['CommonName'].values[0]
    fish_latin_name = df[df['id'] == fish_id]['LatinName'].values[0]
    fish_details = df[df['id'] == fish_id]['Narrative'].values[0]

    fish_desc = ('Common Name: ' + fish_common_name + '\n' + 'Latin Name: ' + fish_latin_name + '\n')

    for desc in fish_details.split('  '):
        fish_desc += desc + '\n'
        
    return fish_desc


print(get_fish(29))