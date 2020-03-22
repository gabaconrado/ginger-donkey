#!/usr/env/python

import sys

from ginger_donkey.entity import PokemonType, PokemonMatchup


def entrypoint():
    '''
    The entrypoint for the system,
    it will parse the arguments and call
    the flow
    '''
    types_arg = sys.argv[1:]
    all_types = PokemonType.setup_all_types()
    matchup = PokemonMatchup([
            p 
            for p in all_types
            if p.name in types_arg
    ])
    print(matchup)


if __name__ == "__main__":
    entrypoint()
