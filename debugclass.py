import inspect

class debug:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def log(self, message):
        if self.enabled:
            # Obtiene de donde fue llamado la funcion
            caller_frame = inspect.currentframe().f_back
            if caller_frame:
                filename = caller_frame.f_code.co_filename.split('\\')[-1]
                line_number = caller_frame.f_lineno
                print(f"[DEBUG] {filename}:{line_number}: {message}")
            else:
                print(f"[DEBUG]: {message}")

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


#EXAMPLE
debugger = debug(enabled=True)
debugger.log("This is a debug message.")