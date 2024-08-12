from controller.controller import Controller
from model import Model
from view.mainview import Mainview
from PySide6.QtWidgets import QApplication, QMainWindow
from view.graphicview import Graphicview


def main() -> None:
    app = QApplication()
    model = Model()
    view = Mainview(model)
    graphicview = Graphicview(model,view)
    controller = Controller(model,view,app,graphicview)
    controller.run()

if __name__ == "__main__":
    main()