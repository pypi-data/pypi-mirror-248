class ProgressBarError(Exception):
    def __init__(self, message="Current step exceeds total steps", *args, **kwargs):
        super().__init__(message, *args, **kwargs)