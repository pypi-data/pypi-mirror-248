from ast import arg
import threading
import time


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def some_function(string):
    while True:
        if thread1.stopped():
            break
        print(string)
        time.sleep(1)


# Usage
thread1 = StoppableThread(target=some_function, args=['text'])
thread1.start()

time.sleep(5)

# When you want to stop the thread
thread1.stop()
