


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=('Toma un archivo de texto con información '
                                         'sobre los depósitos y calcula la ciudad óptima '
                                         'donde ubicar la fábrica mediante el algoritmo '
                                         'de Johnson.'))

    parser.add_argument('archivo', metavar='archivo.txt', type=str,
                        help=('path al archivo que contiene la información '
                        'sobre los contenedores.'))

    args = parser.parse_args()



