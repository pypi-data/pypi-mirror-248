import os

from . import utils


def test():
    utils.log_action("Launching test")

    os.system("cargo test")
