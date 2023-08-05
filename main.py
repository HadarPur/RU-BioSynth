from execution.terminal import *
from execution.app import *


def gui():
    return


def main():
    if __name__ == "__main__":
        # for development testing
        App().run()
    else:
        Terminal(sys.argv[1:]).run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by the user.")