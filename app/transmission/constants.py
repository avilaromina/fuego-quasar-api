# Satellites choices
# TODO: make ChoiceFields Case-insensitive
SAT_CHOICES = [
    'kenobi',
    'Kenobi',
    'KENOBI',
    'skywalker',
    'Skywalker',
    'SKYWALKER',
    'sato',
    'Sato',
    'SATO',
]

# Satellites names
SATELLITES_NAMES = ['kenobi', 'skywalker', 'sato']

# Satellites coordinates
KENOBI_COORD = [-500, -200]
SKYWALKER_COORD = [100, -100]
SATO_COORD = [500, 100]


SATELLITES = {
    'kenobi': KENOBI_COORD,
    'skywalker': SKYWALKER_COORD,
    'sato': SATO_COORD
}

# Temporary satellite reception
# TODO: Create a cache memory for this values
tmp_transmissions = {
    'kenobi': None,
    'skywalker': None,
    'sato': None,
}
