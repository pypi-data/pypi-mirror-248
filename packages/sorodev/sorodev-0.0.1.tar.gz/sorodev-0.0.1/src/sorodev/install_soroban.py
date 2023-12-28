import os
import subprocess


def install_soroban():
    print("Installing soroban")
    # os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    os.system("rustup target add wasm32-unknown-unknown")
    os.system("cargo install --locked --version 20.1.1 soroban-cli")
    # os.system('echo "source <(soroban completion --shell bash)" >> ~/.bashrc')
