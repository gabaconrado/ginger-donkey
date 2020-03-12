import pytest


@pytest.fixture
def sys_argv_mock(mocker):
    argv_mock = mocker.patch('sys.argv', ['poke_counter.py', 'a'])
    yield argv_mock


@pytest.fixture
def find_best_type_mock(mocker):
    best_type_against_mock = mocker.patch(
        'src.ginger_donkey.poke_counter.find_best_type_against'
    )
    best_type_against_mock.return_value = 'b'
    yield best_type_against_mock


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
        'electric,rock,ground\n'
        'water,electric,grass\n'
        'dragon,dragon,ice\n'
    )
    read_m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    yield read_m


@pytest.fixture
def pokemon_matchup_mock():
    from src.ginger_donkey.entity import PokemonType, PokemonMatchup
    p = PokemonMatchup([PokemonType('tipo', [])])
    p.super_effectives = ['tipo1', 'tipo2']
    p.ultra_effectives = ['tipo3']
    p.not_effectives = ['tipo4']
    p.immunes = ['tipo5']
    yield p


def test_entrypoint(
    sys_argv_mock,
    find_best_type_mock,
    print_mock
):
    # given
    from src.ginger_donkey.poke_counter import entrypoint
    # when
    entrypoint()
    # then
    find_best_type_mock.assert_called_once_with(sys_argv_mock[1:])
    print_mock.assert_called_once_with(find_best_type_mock.return_value)


def test_find_best_type_against(
    all_types_mock
):
    # given
    from src.ginger_donkey.poke_counter import find_best_type_against
    # when
    best_types = find_best_type_against('electric')
    # then
    assert best_types == [['ground', 'rock']]


def test_setup_all_types(read_config_file_mock):
    # given
    from src.ginger_donkey.entity import PokemonType
    # when
    all_types = PokemonType.setup_all_types()
    assert all_types == [
        PokemonType('electric', ['rock', 'ground']),
        PokemonType('water', ['electric', 'grass']),
        PokemonType('dragon', ['dragon', 'ice']),
    ]


def test_build_matchup_output(pokemon_matchup_mock):
    # given
    expected_output = ('Pokemon Matchup (Tipo):\n'
                       '\tSuper effective (2.0x): Tipo1, Tipo2\n'
                       '\tUltra effective (4.0x): Tipo3\n'
                       '\tNot effective   (0.5x): Tipo4\n'
                       '\tImmune          (0.0x): Tipo5\n')
    # when
    matchup_output = pokemon_matchup_mock._build_matchup_output()
    # then
    assert matchup_output == expected_output


def test_list_to_comma_upper_case_string():
    # given
    from src.ginger_donkey.entity import _list_to_comma_upper_case_string
    # when
    output = _list_to_comma_upper_case_string(['ab', 'cd'])
    # then
    assert output == 'Ab, Cd'

