import os

from . import utils


def make_binding(contract_name, network=None):
    cfg = utils.load_config()

    if network == None:
        network = cfg["default_network"]

    utils.log_action(f"Creating binding for {contract_name} on {network}")

    cmd = f"""\
        soroban contract bindings typescript\
            --network {network}\
            --contract-id $(cat .soroban/{contract_name}-id)\
            --output-dir node_modules/{contract_name}-client\
            --overwrite
    """
    _, error = utils.call(cmd)

    if error:
        utils.exit_error(error)

    print("Done")
