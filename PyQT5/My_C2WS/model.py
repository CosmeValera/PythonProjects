class MyModel:
    def __init__(self):
        self._data = "My data"

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data
