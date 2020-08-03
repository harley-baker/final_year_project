# Basic script to run model training
# Usage: train.py -i parsed_datasets/bots_and_humans.csv -o models/test.h5 -e 1000
import sys
from utils.neural_net import train_model
from getopt import getopt, GetoptError


def main(argv):
    input_file = ''
    output_file = ''
    epochs = 250

    try:
        opts, args = getopt(argv, 'hi:o:e')
    except GetoptError:
        print('train.py -i <input file> -o <output file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('train.py -i <input file(s) comma separated> -o <output file>')
            sys.exit()
        elif opt in '-i':
            input_file = arg
        elif opt in '-o':
            output_file = arg
        elif opt in '-e':
            epochs = arg

    train_model(input_file, output_file, epochs=epochs)


if __name__ == "__main__":
    main(sys.argv[1:])
