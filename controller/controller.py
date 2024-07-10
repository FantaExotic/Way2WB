from model import Model
from view.view import View
from controller.maincontroller import Maincontroller
from controller.watchlistcontroller import Watchlistcontroller

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.maincontroller = Maincontroller(model=model, view=view)
        self.watchlistcontroller = Watchlistcontroller(model=model, view=view)

    def run(self) -> None:
        self.view.root.mainloop()