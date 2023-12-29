import argparse

import sorodev
from . import utils


def parseCommand():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action",
        type=str,
        help="Can be install-app, add-contract, build, test, deploy, invoke",
    )

    args, _ = parser.parse_known_args()

    if args.action == "add-contract":
        parser.add_argument("contract_name", type=str, help="Name of the new contract")
    elif args.action == "add-account":
        parser.add_argument("account_name", type=str, help="Name of the new account")
    elif args.action == "make-binding":
        parser.add_argument("contract_name", type=str, help="Name of the contract")
        parser.add_argument("--network", default=None, help="Specify the network")
    elif args.action == "deploy":
        parser.add_argument("contract_name", type=str, help="Name of the contract")
        parser.add_argument("--network", default=None, help="Specify the network")
    elif args.action == "invoke":
        parser.add_argument("contract_name", type=str, help="Name of the contract")
        parser.add_argument("function", type=str, help="Name of the fuction to call")
        parser.add_argument(
            "--args", default="", help="Arguments to pass to the function call"
        )
        parser.add_argument(
            "--account", default=None, help="Account performing the call"
        )
        parser.add_argument("--network", default=None, help="Specify the network")

    return parser.parse_args()


def main():
    args = parseCommand()

    if args.action != "install":
        utils.check_in_sorodev_project()

    if args.action == "install":
        sorodev.install()
    elif args.action == "add-contract":
        sorodev.add_contract(args.contract_name)
    elif args.action == "add-account":
        sorodev.add_account(args.account_name)
    elif args.action == "build":
        sorodev.build()
    elif args.action == "test":
        sorodev.test()
    elif args.action == "make-binding":
        sorodev.make_binding(args.contract_name, args.network)
    elif args.action == "deploy":
        sorodev.deploy(args.contract_name, args.network)
    elif args.action == "invoke":
        sorodev.invoke(
            args.contract_name, args.function, args.args, args.network, args.account
        )
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
