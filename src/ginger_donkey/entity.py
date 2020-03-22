class PokemonType():

    def __init__(
        self, name, weaknesses=[], strengths=[], immunities=[]
    ):
        self.name = name
        self.weaknesses = weaknesses.copy()
        self.strengths = strengths.copy()
        self.immunities = immunities.copy()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.weaknesses == other.weaknesses,
            self.strengths == other.strengths,
            self.immunities == other.immunities
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
                tokens = line.split('|')
                tokens = list(map(str.rstrip, tokens))
                poke_type = PokemonType(
                    name=tokens[0],
                    weaknesses=[
                        t for t in tokens[1].split(',')
                        if tokens[1]
                    ],
                    strengths=[
                        t for t in tokens[2].split(',')
                        if tokens[2]
                    ],
                    immunities=[
                        t for t in tokens[3].split(',')
                        if tokens[3]
                    ]
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
        (self.super_effectives, 
         self.ultra_effectives,
         self.not_effectives,
         self.immunes) = self._evaluate_matchup()
         

    def __str__(self):
        return self._build_matchup_output()

    def _evaluate_matchup(self):        
        def _evaluate_super_effectives():
            return set.union(*(
                set(t.weaknesses)
                for t in self.types
            ))
        def _evaluate_ultra_effectives():
            return (
                set.intersection(*(
                    set(t.weaknesses) 
                    for t in self.types                
                ))
                if len(self.types) > 1
                else set()
            )
        def _evaluate_not_effectives():
            return set.union(*(
                set(t.strengths)
                for t in self.types
            ))
        def _evaluate_immunities():
            return set.union(*(
                set(t.immunities)
                for t in self.types
            ))                

        immunes = _evaluate_immunities()
        not_effectives = (
            _evaluate_not_effectives() -
            immunes
        )
        ultra_effectives = (
            _evaluate_ultra_effectives() -
            immunes
        )        
        super_effectives = (
            _evaluate_super_effectives() - 
            immunes -
            ultra_effectives
        )
        ultra_and_not = set.intersection(ultra_effectives, not_effectives)
        super_and_not = set.intersection(super_effectives, not_effectives)
        if ultra_and_not:
            ultra_effectives -= ultra_and_not
            not_effectives -= ultra_and_not
            super_effectives += ultra_and_not
        if super_and_not:
            super_effectives -= super_and_not
            not_effectives -= super_and_not        

        return (
            super_effectives,
            ultra_effectives,
            not_effectives,
            immunes
    )
            

    def _build_matchup_output(self):
        from .util import list_to_comma_upper_case_string
        return PokemonMatchup.OUTPUT_FORMAT.format(
            types=list_to_comma_upper_case_string(
                [str(t) for t in self.types]
            ),
            super_effectives=list_to_comma_upper_case_string(
                self.super_effectives
            ),
            ultra_effectives=list_to_comma_upper_case_string(
                self.ultra_effectives
            ),
            not_effectives=list_to_comma_upper_case_string(
                self.not_effectives
            ),
            immunes=list_to_comma_upper_case_string(
                self.immunes
            )
        )
