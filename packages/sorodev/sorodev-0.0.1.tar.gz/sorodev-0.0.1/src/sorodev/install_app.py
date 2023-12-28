from pathlib import Path
import os


from . import add_contract
from . import account
from . import utils
from . import constants


def write_soroban_dev_config(app_path, name):
    data = {
        "main_contract": name,
        "default_network": "testnet",
        "accounts": ["alice"],
        "default_account": "alice",
        "binding_type": "typescript",
    }

    target = app_path.joinpath(constants.SOROBAN_DEV_FILE_NAME)
    utils.write_json(target, data)


def write_gitignore(app_path):
    lines = """\
        .soroban/
        target/
    """

    target = app_path.joinpath(".gitignore")
    utils.write_lines(target, lines)


def write_standalone_cargo_toml(app_path):
    lines = """\
        [workspace]
        resolver = "2"
        members = ["contracts/*"]

        [workspace.dependencies]
        soroban-sdk = "20.0.0"

        [profile.release]
        opt-level = "z"
        overflow-checks = true
        debug = 0
        strip = "symbols"
        debug-assertions = false
        panic = "abort"
        codegen-units = 1
        lto = true

        [profile.release-with-logs]
        inherits = "release"
        debug-assertions = true
    """

    target = app_path.joinpath("Cargo.toml")
    utils.write_lines(target, lines)


def install_app(name):
    utils.log_action(f"Installing standalone app: {name}")

    app_path = Path(name)
    app_path.mkdir(exist_ok=True)

    contract_addr_path = app_path.joinpath(".soroban")
    contract_addr_path.mkdir(exist_ok=True)

    write_soroban_dev_config(app_path, name)
    write_standalone_cargo_toml(app_path)
    write_gitignore(app_path)

    os.chdir(app_path)
    add_contract.add_contract(name)
    # account.add_account('alice')
