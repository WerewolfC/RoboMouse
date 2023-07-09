"""RoboMouse app v1.0"""
import logging
from robomouse.presenter import Presenter
from robomouse.model import Model
from robomouse.gui import Gui
from robomouse.utilities import config_logger


def main():
    """Main app function"""
    app_logger = config_logger(logging.getLogger(__name__))
    app_logger.info('Appp log started')

    model = Model()
    view = Gui("flatly")
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == '__main__':
    main()
