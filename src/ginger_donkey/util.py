def list_to_comma_upper_case_string(input_list):
    return ('{}, ' * len(input_list)).format(
        *[f'{x.capitalize()}' for x in sorted(input_list)]
    )[:-2]
