_timers = {}


class Timer:

    @staticmethod
    def add(key):
        _timers[key] = 0

    @staticmethod
    def remove(key):
        del _timers[key]

    @staticmethod
    def get(key):
        return _timers[key]

    @staticmethod
    def tick():

        for key, _ in _timers.items():
            _timers[key] += 1
