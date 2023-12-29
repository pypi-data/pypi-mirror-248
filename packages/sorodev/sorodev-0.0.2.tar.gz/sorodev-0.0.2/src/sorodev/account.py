from . import utils


def create_account(name):
    cmd = f"soroban config identity generate {name}"
    _, error = utils.call(cmd)
    if error:
        utils.exit_error(error)

    cmd = f"soroban config identity address {name}"

    address, error = utils.call(cmd)
    if error:
        utils.exit_error(error)

    print(f"Account {name} created with address {address.strip()}")


def fund_account(name, network=None):
    cfg = utils.load_config()
    if network == None:
        network = cfg["default_network"]

    cmd = f"soroban config identity fund {name} --network {network}"

    _, error = utils.call(cmd)
    if error:
        utils.exit_error(error)

    print(f"Funded account {name} on {network}")


def add_account(name):
    utils.log_action(f"Adding account {name}")

    create_account(name)
    fund_account(name)

    cfg = utils.load_config()
    if name not in cfg["accounts"]:
        cfg["accounts"].append(name)
    utils.save_config(cfg)
