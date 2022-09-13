import json

# list of Arcana existed
ARCANA = [
    'Fool',
    'Jester',
    'Magician',
    'Councillor',
    'Priestess',
    'Empress',
    'Emperor',
    'Hierophant',
    'Lovers',
    'Chariot',
    'Justice',
    'Hermit',
    'Fortune',
    'Strength',
    'Hunger',
    'Hanged Man',
    'Death',
    'Temperance',
    'Devil',
    'Tower',
    'Star',
    'Moon',
    'Sun',
    'Judgement',
    'Aeon',
    'World',
    'Faith'
]

def get_Arcana():
    # convert ARCANA.json into a dict
    with open('data/ARCANA.json', 'r') as f:
        arcana_lst = json.load(f)
    return arcana_lst

# Arcana json generator
'''
def Arcana_Map():
    with open('Data/ARCANA.json', 'w) as f:
        arcana = {}
        for x in ARCANA:
            arcana[x] = {
                'URL': 'https://static.wikia.nocookie.net/megamitensei/images/5/53/Fool-0.png/revision/latest?cb=20160404201043'
            }
        print(arcana)
        json.dump(arcana, f, indent=2)
'''