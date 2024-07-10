from controller.controller import Controller
from model import Model
from view.view import View

def main() -> None:
    model = Model()
    view = View(model)
    controller = Controller(model,view)
    controller.run()

if __name__ == "__main__":
    main()