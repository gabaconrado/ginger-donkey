import pytest


@pytest.fixture
def sys_argv_mock(mocker):
    argv_mock = mocker.patch('sys.argv', ['poke_counter.py', 'a'])
    yield argv_mock


@pytest.fixture
def print_mock(mocker):
    print_m = mocker.patch('builtins.print')
    yield print_m


@pytest.fixture
def all_types_mock(mocker):
    from src.ginger_donkey.entity import PokemonType
    all_types_m = mocker.patch(
        'src.ginger_donkey.entity.PokemonType.setup_all_types',
        return_value = [PokemonType('electric', ['ground', 'rock'])]
    )
    yield all_types_m


@pytest.fixture()
def read_config_file_mock(mocker):
    data = (
        'normal|fighting||ghost\n'
        'electric|ground|flying,steel,electric|\n'
        'fairy|poison,steel|fighting,bug,dark|dragon\n'
    )
    read_m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    yield read_m


@pytest.fixture
def pokemon_matchup_already_setup():
    from src.ginger_donkey.entity import PokemonType, PokemonMatchup
    p = PokemonMatchup([PokemonType('tipo', [])])
    p.super_effectives = ['tipo1', 'tipo2']
    p.ultra_effectives = ['tipo3']
    p.not_effectives = ['tipo4']
    p.immunes = ['tipo5']
    yield p


@pytest.fixture
def pokemon_type_mock(mocker):
    yield mocker.patch(
        'src.ginger_donkey.poke_counter.PokemonType',
        autospec=True
    )

@pytest.fixture
def pokemon_matchup_mock(mocker):
    yield mocker.patch(
        'src.ginger_donkey.poke_counter.PokemonMatchup',
        autospec=True
    )


def test_entrypoint(
    sys_argv_mock,
    pokemon_type_mock,
    pokemon_matchup_mock,
    print_mock
):
    # given
    from src.ginger_donkey.poke_counter import entrypoint
    # when
    entrypoint()
    # then
    pokemon_type_mock.setup_all_types.assert_called_once
    pokemon_matchup_mock.assert_called_once_with([])
    print_mock.assert_called_once_with(pokemon_matchup_mock.return_value)


def test_setup_all_types(read_config_file_mock):
    # given
    from src.ginger_donkey.entity import PokemonType
    # when
    all_types = PokemonType.setup_all_types()
    assert all_types[0] == PokemonType(
            name='normal',
            weaknesses=['fighting'],
            immunities=['ghost']
    )
    assert all_types[1] == PokemonType(
            name='electric',
            weaknesses=['ground'],
            strengths=['flying','steel','electric']
    )
    assert all_types[2] == PokemonType(
            name='fairy',
            weaknesses=['poison', 'steel'],
            strengths=['fighting', 'bug', 'dark'], 
            immunities=['dragon']
    )


def test_build_matchup_output(pokemon_matchup_already_setup):
    # given
    expected_output = ('Pokemon Matchup (Tipo):\n'
                       '\tSuper effective (2.0x): Tipo1, Tipo2\n'
                       '\tUltra effective (4.0x): Tipo3\n'
                       '\tNot effective   (0.5x): Tipo4\n'
                       '\tImmune          (0.0x): Tipo5\n')
    # when
    matchup_output = pokemon_matchup_already_setup._build_matchup_output()
    # then
    assert matchup_output == expected_output


def test_list_to_comma_upper_case_string():
    # given
    from src.ginger_donkey.util import list_to_comma_upper_case_string
    # when
    output = list_to_comma_upper_case_string(['cd', 'ab'])
    # then
    assert output == 'Ab, Cd'


@pytest.mark.parametrize(
    'weaknesses, expected',
    [
        (
            [['tipo3', 'tipo4'], ['tipo4', 'tipo5']],
            ({'tipo3', 'tipo5'}, {'tipo4'})
        ),
        (
            [['tipo1']],
            ({'tipo1'}, set())
        ),
        (
            [['tipo1'], ['tipo1']],
            (set(), {'tipo1'})
        )
    ],
    ids = [
        'both',
        'only super effective',
        'only ultra effective'
    ]
)
def test_evaluate_matchup(weaknesses, expected):
    # given
    from src.ginger_donkey.entity import PokemonMatchup, PokemonType
    matchup = PokemonMatchup([
        PokemonType('name', t)
        for t in weaknesses
    ])
    assert (
        (matchup.super_effectives, matchup.ultra_effectives) == 
        expected
    )
