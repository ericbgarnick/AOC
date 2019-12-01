import time


class Metric:
    def __init__(self, name: str):
        self.name = name
        self.max_time = 0
        self.min_time = float('inf')
        self.mean_time = 0.0
        self.timings = []
        self.num_timings = 0
        self.total_time = 0

        self._start = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        new_time = time.perf_counter() - self._start

        self.max_time = max(self.max_time, new_time)
        self.min_time = min(self.min_time, new_time)

        self.total_time += new_time
        self.timings.append(new_time)
        self.num_timings += 1

        self.mean_time = self.total_time / self.num_timings

    def __str__(self):
        return ("Metric: {}\nMin time: {}\nMax time: {}"
                "\nMean time: {}\nNum timings: {}\nTotal time: {}"
                .format(self.name, self.min_time, self.max_time,
                        self.mean_time, self.num_timings, self.total_time))

    __repr__ = __str__
