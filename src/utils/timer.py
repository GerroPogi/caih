import time,threading

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.started=False
        self.ended=False

    def start(self, duration_in_seconds:float=1):
        threading.Thread(target=self._start, args=(duration_in_seconds,)).start()
        return self.started

    def get_time_elapsed (self):
        return time.time()-self.start_time
    
    def _start(self, duration:float=1):
        self.start_time = time.time()
        self.started=True
        self.end_time = time.time()+duration
        while not self.ended:
            time.sleep(duration)
            self.end_time = time.time()
            self.ended=True

    def stop(self):
        self.end_time = time.time()
        return self.end_time - self.start_time

    def get_duration(self):
        return self.end_time - self.start_time
    
    def get_time_left(self):
        return self.end_time - time.time()

if __name__ == "__main__":
    timer = Timer()
    timer.start(10)
    print(f"### Time left: {time.strftime('%M:%S', time.gmtime(timer.get_duration() -timer.get_time_elapsed()))}")