import pytest

from subprocess import run

OUTPUTS = {
    'electric': ('Pokemon Matchup (Electric):'
                 '\tSuper effective (2.0x): Ground, Rock\n'
                 '\tUltra effective (4.0x):\n'
                 '\tNot effective   (0.5x):\n'
                 '\tImmune          (0.0x):\n'),
    'fairy dragon': ('Pokemon Matchup (Fairy, Dragon):'
                     '\tSuper effective (2.0x): Ice, Dragon, Fairy, '
                                               'Poison, Steel\n'
                     '\tUltra effective (4.0x):\n'
                     '\tNot effective   (0.5x):\n'
                     '\tImmune          (0.0x):\n'),
    'water': ('Pokemon Matchup (Water):'
              '\tSuper effective (2.0x): Electric, Grass\n'
              '\tUltra effective (4.0x):\n'
              '\tNot effective   (0.5x):\n'
              '\tImmune          (0.0x):\n'),
    'dark': ('Pokemon Matchup (Dark):'
             '\tSuper effective (2.0x): Fighting, Bug, Fairy\n'
             '\tUltra effective (4.0x):\n'
             '\tNot effective   (0.5x):\n'
             '\tImmune          (0.0x):\n'),
}

@pytest.mark.parametrize(
    'type_input, expected',
    [
        (_input, _output)
        for _input, _output in OUTPUTS.items()
    ],
    ids = [
        'Electric',
        'Fairy + Dragon',
        'Water',
        'Dark'
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
    assert proc_call.stdout.rstrip() == expected
    # All good! He won!
    # Thanks ginger-donkey!
