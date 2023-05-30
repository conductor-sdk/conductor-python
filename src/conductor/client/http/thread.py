import threading


class AwaitableThread(threading.Thread):
    def wait(self):
        self.join()
