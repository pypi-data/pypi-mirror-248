from . import utils


def invoke(
    function_name, function_args={}, contract_name=None, network=None, source=None
):
    if type(function_args) == dict:
        function_args = " ".join(
            [f"--{key} {val}" for key, val in function_args.items()]
        )

    cfg = utils.load_config()

    if contract_name == None:
        contract_name = cfg["main_contract"]

    if network == None:
        network = cfg["default_network"]

    if source == None:
        source = cfg["default_account"]

    utils.log_action(
        f'Invoking latest "{contract_name}" contract on {network} from {source} with "{function_name} {function_args}"'
    )

    cmd = f"cat .soroban/{contract_name}-id"
    contract_address, error = utils.call(cmd)
    if error:
        utils.exit_error(f"No deployment found")

    print(f"Contract address: {contract_address}")

    cmd = f"""\
        soroban contract invoke \
            --id {contract_address} \
            --source {source} \
            --network {network} \
            -- \
                {function_name} \
                {function_args}
    """

    output, error = utils.call(cmd)

    if error:
        utils.exit_error(error)

    print(output)
