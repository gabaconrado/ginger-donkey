#!/usr/env/python

import sys

from entity import PokemonType


def find_best_type_against(target_types):
    '''
    Function that will search for the best type matchup
    for a given type
    args:
    (list) target_types: List of types
    return:
    (list) best_types: The best types matchup
    '''
    return [
        t.weaknesses
        for t in PokemonType.setup_all_types() if
        t.name in target_types
    ]


def entrypoint():
    '''
    The entrypoint for the system,
    it will parse the arguments and call
    the flow
    '''
    types_arg = sys.argv[1:]
    best_types = find_best_type_against(types_arg)
    print(best_types)


if __name__ == "__main__":
    entrypoint()
