#timer.py
import datetime

class Timer:
    def __init__(self):
        self.start_time = None

    def start_stop(self):
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
            print(f"Timer started at {self.start_time}")
            return self.start_time
        else:
            total_time = datetime.datetime.now() - self.start_time
            print(f"Timer stopped. Total time: {total_time}")
            self.start_time = None
            return None

    def get_elapsed_time(self):
        if self.start_time is None:
            return None
        return datetime.datetime.now() - self.start_time
