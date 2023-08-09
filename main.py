from executions.terminal_execution import *
from executions.app_execution import *
from executions.gui_execution import *


def main():
    if __name__ == "__main__":
        # for development testing
        App().execute()
    else:
        Terminal(sys.argv[1:]).execute()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by the user.")