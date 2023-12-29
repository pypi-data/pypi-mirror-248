from pathlib import Path
import os


from . import add_contract
from . import utils
from . import constants


def write_soroban_dev_config():
    data = {
        "main_contract": None,
        "default_network": "testnet",
        "accounts": ["alice"],
        "default_account": "alice",
        "binding_type": "typescript",
    }

    target = Path(constants.SOROBAN_DEV_FILE_NAME)
    utils.write_json(target, data)


def write_gitignore():
    lines = """\
        .soroban/
        target/
    """

    target = Path(".gitignore")
    utils.write_lines(target, lines)


def write_standalone_cargo_toml():
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

    target = Path("Cargo.toml")
    utils.write_lines(target, lines)


def install():
    if utils.is_in_sorodev_project():
        utils.exit_error("Sorodev project already initialized")

    utils.log_action(f"Installing in: {os.getcwd()}")

    contract_addr_path = Path(".soroban")
    contract_addr_path.mkdir(exist_ok=True)

    write_soroban_dev_config()
    write_standalone_cargo_toml()
    write_gitignore()

    print("Done")
