import pytest

from subprocess import run

@pytest.mark.parametrize(
    'type_input, expected',
    [
        ('electric', b"[['ground']]"),
        ('fairy dragon', b"[['ice', 'dragon', 'fairy'], ['poison', 'steel']]"),
        ('water', b"[['electric', 'grass']]"),
        ('dark', b"[['fighting', 'bug', 'fairy']]")
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
