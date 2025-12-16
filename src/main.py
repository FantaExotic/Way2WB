from controller.controller import Controller
from model.model import Model
from view.mainview import Mainview
from PySide6.QtWidgets import QApplication
from view.graphicview import Graphicview
import argparse
import sys

def main() -> None:

    parser = argparse.ArgumentParser(description="Way2WB Tool")
    parser.add_argument("--testmode", help="Testmode to perform basic tests without GUI (e.g. for testing in CI/CD pipeline)", action="store_true")
    args = parser.parse_args()

    app = QApplication()
    model = Model()
    #startupview = Startupview(model)
    mainview = Mainview(model)
    graphicview = Graphicview(model,mainview)
    controller = Controller(model,mainview,app,graphicview)

    if args.testmode:
        print("Application running in Testmode. controller.run() will not be called")
        sys.exit(0)
    controller.run()

if __name__ == "__main__":
    main()