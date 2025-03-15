import sys

from chiplet import Chip

def main() -> None:
    """
    Main Function will execute the Chip8 Emulator
    :return: None
    """
    # get the arguments
    args = sys.argv[1:]
    c = Chip(args[0])

main()