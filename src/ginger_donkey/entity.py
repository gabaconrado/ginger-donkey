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
