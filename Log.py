class Log:
    def __init__(self, debug_on):
        self.DEBUG = debug_on

    def log(self, msg):
        if self.DEBUG:
            print(msg)

    def error(self, msg):
        print(msg)
