import pytest

from subprocess import run

OUTPUTS = {
    'electric': ('Pokemon Matchup (Electric):\n'
                 '\tSuper effective (2.0x): Ground\n'
                 '\tUltra effective (4.0x): \n'
                 '\tNot effective   (0.5x): Electric, Flying, Steel\n'
                 '\tImmune          (0.0x): \n\n'),
    'fairy dragon': ('Pokemon Matchup (Dragon, Fairy):\n'
                     '\tSuper effective (2.0x): Fairy, Ice, '
                                               'Poison, Steel\n'
                     '\tUltra effective (4.0x): \n'
                     '\tNot effective   (0.5x): Bug, Dark, Electric, '
                                               'Fighting, Fire, '
                                               'Grass, Water\n'
                     '\tImmune          (0.0x): Dragon\n\n'),
    'water': ('Pokemon Matchup (Water):\n'
              '\tSuper effective (2.0x): Electric, Grass\n'
              '\tUltra effective (4.0x): \n'
              '\tNot effective   (0.5x): Fire, Ice, Steel, Water\n'
              '\tImmune          (0.0x): \n\n'),
    'dark': ('Pokemon Matchup (Dark):\n'
             '\tSuper effective (2.0x): Bug, Fairy, Fighting\n'
             '\tUltra effective (4.0x): \n'
             '\tNot effective   (0.5x): Dark, Ghost\n'
             '\tImmune          (0.0x): Psychic\n\n'),
    'water flying': ('Pokemon Matchup (Flying, Water):\n'
             '\tSuper effective (2.0x): Rock\n'
             '\tUltra effective (4.0x): Electric\n'
             '\tNot effective   (0.5x): Bug, Fighting, Fire, Steel, '
                                       'Water\n'
             '\tImmune          (0.0x): Ground\n\n'),
}

@pytest.mark.parametrize(
    'type_input, expected',
    [
        (_input, _output)
        for _input, _output in OUTPUTS.items()
    ],
    ids = [
        'electric',
        'fairy + dragon',
        'water',
        'dark',
        'water + flying'
    ]
)
def test_counter_type(type_input, expected):
    # Jonas wants to know the types of pokémon are
    # good against their opponents.
    # He is fighting against an electric Pokémon, so
    # he calls the utility passing it as parameter
    args = ['python', 'src/ginger_donkey/poke_counter.py']
    args += type_input.split(' ')
    proc_call = run(
        args,
        capture_output=True
    )
    # He will receive the types that are strong against
    # electric.
    assert proc_call.returncode == 0
    assert proc_call.stdout.decode('utf-8') == expected
    # All good! He won!
    # Thanks ginger-donkey!
