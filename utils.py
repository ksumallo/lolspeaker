class Log:
    PREFIX_DEBUG = "DEBUG"
    PREFIX_INFO = "INFO"
    PREFIX_WARN = "WARN"
    PREFIX_ERROR = "ERROR"

    COLOR_DEBUG = '\033[32m'
    COLOR_INFO = '\033[34m'
    COLOR_WARN = '\033[33m'
    COLOR_ERROR = '\033[31m'
    COLOR_CLEAR = '\033[0m'

    show_logs = True

    @staticmethod
    def show(enable: bool):
        Log.show_logs = enable

    @staticmethod
    def d(message: str):
        if Log.show_logs:
            print(Log.COLOR_DEBUG, end='')
            print(f"[{Log.PREFIX_DEBUG}]", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def i(message: str):
        if Log.show_logs:
            print(Log.COLOR_INFO, end='')
            print(f"[{Log.PREFIX_INFO}]", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def w(message: str):
        if Log.show_logs:
            print(Log.COLOR_WARN, end='')
            print(f"[{Log.PREFIX_WARN}]", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def e(message: str):
        if Log.show_logs:
            print(Log.COLOR_ERROR, end='')
            print(f"[{Log.PREFIX_ERROR}]", message)
            print(Log.COLOR_CLEAR, end='')