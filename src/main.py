from controller.controller import Controller
from model.model import Model
from view.mainview import Mainview
#from view.startupview import Startupview
from PySide6.QtWidgets import QApplication
from view.graphicview import Graphicview

def main() -> None:
    app = QApplication()
    model = Model()
    #startupview = Startupview(model)
    mainview = Mainview(model)
    graphicview = Graphicview(model,mainview)
    controller = Controller(model,mainview,app,graphicview)
    controller.run()

if __name__ == "__main__":
    main()