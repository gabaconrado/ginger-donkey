def _list_to_comma_upper_case_string(input_list):
    return ('{}, ' * len(input_list)).format(
        *[f'{x.capitalize()}' for x in input_list]
    )[:-2]

class PokemonType():

    def __init__(self, name, weaknesses=[]):
        self.name = name
        self.weaknesses = weaknesses.copy()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.weaknesses == other.weaknesses
        ])

    @classmethod
    def setup_all_types(cls):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_dir = os.path.join(os.path.dirname(dir_path), 'util')
        config_name = 'poke-config.txt'
        config_path = os.path.join(config_dir, config_name)
        poke_types = []
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                tokens = line.split(',')
                tokens = list(map(str.rstrip, tokens))
                poke_type = PokemonType(
                    tokens.pop(0),
                    weaknesses=tokens
                )
                poke_types.append(poke_type)
        return poke_types


class PokemonMatchup():

    OUTPUT_FORMAT = ('Pokemon Matchup ({types}):\n'
                     '\tSuper effective (2.0x): {super_effectives}\n'
                     '\tUltra effective (4.0x): {ultra_effectives}\n'
                     '\tNot effective   (0.5x): {not_effectives}\n'
                     '\tImmune          (0.0x): {immunes}\n')

    def __init__(self, types):
        self.types = types.copy()
        self.super_effectives = []
        self.ultra_effectives = []
        self.not_effectives = []
        self.immunes = []



    def _build_matchup_output(self):
        return PokemonMatchup.OUTPUT_FORMAT.format(
            types=_list_to_comma_upper_case_string(
                [str(t) for t in self.types]
            ),
            super_effectives=_list_to_comma_upper_case_string(
                self.super_effectives
            ),
            ultra_effectives=_list_to_comma_upper_case_string(
                self.ultra_effectives
            ),
            not_effectives=_list_to_comma_upper_case_string(
                self.not_effectives
            ),
            immunes=_list_to_comma_upper_case_string(
                self.immunes
            )
        )
