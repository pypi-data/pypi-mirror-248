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

    if args.action == "install-app":
        parser.add_argument("name", type=str, help="Name of the app")
    elif args.action == "add-contract":
        parser.add_argument("contract_name", type=str, help="Name of the new contract")
    elif args.action == "make-binding":
        parser.add_argument("contract_name", type=str, help="Name of the contract")
        parser.add_argument("--network", default=None, help="Specify the network")
    elif args.action == "deploy":
        parser.add_argument("--network", default=None, help="Specify the network")
    elif args.action == "invoke":
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

    if args.action not in ["install-soroban", "install-app"]:
        utils.check_in_sorodev_project()

    if args.action == "install-soroban":
        sorodev.install_soroban()
    elif args.action == "install-app":
        sorodev.install_app(args.name)
    elif args.action == "build":
        sorodev.build()
    elif args.action == "test":
        sorodev.test()
    elif args.action == "make-binding":
        sorodev.make_binding(args.contract_name, args.network)
    elif args.action == "add-contract":
        sorodev.add_contract(args.contract_name)
    elif args.action == "deploy":
        sorodev.deploy(args.network)
    elif args.action == "invoke":
        sorodev.invoke(args.function, args.args, args.network, args.account)
    else:
        print("Unknown command")


main()
