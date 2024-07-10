from model import Model
from view.view import View

class Maincontroller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.mainview
        self.bind_view_controller()

    def bind_view_controller(self):
        self.view.mainview.button_configWatchlist.configure(command=self.handle_button_configWatchlist)

    def handle_button_configWatchlist(self):
        self.view.setWatchlistview()
