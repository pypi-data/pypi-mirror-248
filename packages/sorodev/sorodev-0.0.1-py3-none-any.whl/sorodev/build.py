
import os

from . import utils


def build():
    utils.log_action('Building contracts')

    os.system('soroban contract build')
