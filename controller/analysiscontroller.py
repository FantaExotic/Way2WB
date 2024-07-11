from model import Model
from view.view import View

class Analysiscontroller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.analysisview
        self.bind_view_controller()
        self.bind_symbolentry_enterpressed()
        self.bind_buttonDelete_method()
        #self.updateListbox()

    def updateListbox(self):
        #TODO fix because it adds all data to listbox again after clicking on "analysis" in mainview
        self.view.analysisview.updateListbox(self.model)

    def bind_view_controller(self):
        self.view.analysisview.button_return.configure(command=self.handle_buttonReturn)

    def handle_buttonReturn(self):
        self.view.setMainview()

    def bind_symbolentry_enterpressed(self):
        self.view.analysisview.enterbutton.configure(command=self.handle_entry_appendWatchlist)

    def bind_buttonDelete_method(self):
        self.view.analysisview.button_delete.configure(command=self.handle_buttonDelete)

    def handle_buttonDelete(self):
        pass

    def handle_entry_appendWatchlist(self):
        pass