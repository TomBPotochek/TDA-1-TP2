



from itertools import repeat
from math import prod


if __name__ == '__main__':
    import argparse
    from argparse import ArgumentParser

    def check_arg_value(val: str) -> int:
        ival = int(val)
        min_val = 3 #creo que menos de esto no tiene sentido
        max_val = 26 #26 letras. ya mas tal vez es mucho
        if ival < min_val:
            raise argparse.ArgumentTypeError(
                        f"should be at least {min_val}. You passed {ival}")
        if ival > max_val:
            raise argparse.ArgumentTypeError(
                        f"should be less than {max_val}. You passed {ival}")
        return ival

    parser = ArgumentParser(description=('genera un archivo de texto '
                                         'con N ciudades y costos asociados a '
                                         'cada par de ciudades.\n'
                                         'los costos son al azar con cada ejecución '
                                         'o puede usarse un seed con el flag '
                                         'correspondiente.'))

    parser.add_argument('num_ciudades', metavar='N', type=check_arg_value,
                        help=('numero de ciudades a generar'))
    parser.add_argument('-s', '--seed', type=int,
                        help='seed to use instead of using a random seed.')

    args = parser.parse_args()

    import random

    N = args.num_ciudades
    
    if args.seed is not None:
        random.seed(args.seed)
    
    get_cost = lambda : random.randint(-100, 100)

    from itertools import product    
    ciudades = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #26

    with open("depositos.txt", "w") as file:
        for i,j in product(range(N), repeat=2):
            if i >= j:
                continue
            file.write(f"{ciudades[i]},{ciudades[j]},{get_cost()}\n")

