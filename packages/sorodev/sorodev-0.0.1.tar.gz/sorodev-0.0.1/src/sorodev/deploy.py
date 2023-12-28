from pathlib import Path

from . import utils


def deploy(contract_name=None, network=None, source=None):
    cfg = utils.load_config()

    if contract_name == None:
        contract_name = cfg["main_contract"]

    if network == None:
        network = cfg["default_network"]

    if source == None:
        source = cfg["default_account"]

    utils.log_action(f"Deploying {contract_name} to {network}")
    cmd = f"""\
        soroban contract deploy \
        --wasm target/wasm32-unknown-unknown/release/{contract_name}.wasm \
        --source {source} \
        --network {network}
    """
    output, error = utils.call(cmd)

    if error:
        utils.exit_error(error)

    contract_address = output.split("\n")[0]

    if contract_address[0] != "C":
        utils.exit_error(f"Could not extract contract address from: {output}")

    print(f"Contract address: {contract_address}")
    Path(f".soroban/{contract_name}-id").write_text(contract_address)
