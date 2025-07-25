class Logger:
    COLORS = {
        "ERROR": "\033[91m",  # Red
        "WARNING": "\033[93m",  # Yellow
        "INFO": "\033[0m",  # default color
        "DEBUG": "\033[92m",  # Green
        "NOTICE": "\033[96m",  # Cyan
        "CRITICAL": "\033[95m",  # Magenta
        "ENDC": "\033[0m",  # Reset to default color
    }

    @staticmethod
    def log(message, level="INFO"):
        color = Logger.COLORS.get(level, Logger.COLORS["ENDC"])
        print(f"{color}{message}{Logger.COLORS['ENDC']}")

    @staticmethod
    def error(message):
        Logger.log("ERROR: " + message, "ERROR")

    @staticmethod
    def warning(message):
        Logger.log(message, "WARNING")

    @staticmethod
    def info(message):
        Logger.log(message, "INFO")

    @staticmethod
    def debug(message):
        Logger.log(message, "DEBUG")

    @staticmethod
    def notice(message):
        Logger.log(message, "NOTICE")

    @staticmethod
    def critical(message):
        Logger.log(message, "CRITICAL")

    @staticmethod
    def space():
        Logger.log('', "INFO")
