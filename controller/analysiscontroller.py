from model import Model
from view.view import View
import tkinter.messagebox as messagebox

class Analysiscontroller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.analysisview
        self.bind_view_controller()
        self.bind_symbolentry_enterpressed()
        self.bind_buttonDelete_method()

    def bind_view_controller(self):
        self.view.analysisview.button_return.configure(command=self.handle_buttonReturn)

    def handle_buttonReturn(self):
        self.view.setMainview()

    def bind_symbolentry_enterpressed(self):
        self.view.analysisview.enterbutton.configure(command=self.handle_entry_method)

    def bind_buttonDelete_method(self):
        self.view.analysisview.button_delete.configure(command=self.handle_buttonDelete)

    def handle_buttonDelete(self):
        index = self.view.analysisview.deleteMethod()
        self.model.remove_method(index)

    #TODO: add selection for multiple methods
    def handle_entry_method(self):
        try:
            _input = int(self.view.analysisview.symbol_var.get())
            self.view.analysisview.add_method(_input)
            temp = dict(method = "MA", value = _input)
            self.model.methods.append(temp)
        except Exception as e:
            # Change appearance to show error
            messagebox.showerror("Error", "Enter integer value!")
