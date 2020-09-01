from .utils.data import generate_data_files
import sys

# Basic script to run pre-processor
def main(argv):
    generate_data_files()


if __name__ == "__main__":
    main(sys.argv[1:])