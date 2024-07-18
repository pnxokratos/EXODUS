import datetime
#This class allows the assistant to give us the current time.
class Time:
    def get_current_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time
