class Observable:
    def __init__(self):
        self._observers = []

    def subscribe(self, method, fn):
        self._observers.append({
            "method": method,
            "fn": fn
        })

    def emit(self, method, data=None):
        for obs in self._observers:
            if obs["method"] == method:
                obs["fn"](self, data)

    def unsubscribe(self, method):
        for obs in self._observers:
            if obs["method"] == method:
                self._observers.remove(obs)
                break