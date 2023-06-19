"""RoboMouse app v1.0
"""

from robomouse.presenter import Presenter
from robomouse.model import Model
from robomouse.gui import Gui


def main():
    """Main app function"""
    model = Model()
    view = Gui("flatly")
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == '__main__':
    main()
