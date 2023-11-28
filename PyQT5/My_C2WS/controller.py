class MyController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def update_data(self, data):
        self._model.set_data(data)
        self._view.update_view(data)
