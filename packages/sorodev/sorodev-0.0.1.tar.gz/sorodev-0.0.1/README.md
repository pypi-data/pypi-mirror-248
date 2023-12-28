# About

Sorodev is a CLI tool and Python package which allows to develop with [Soroban](https://soroban.stellar.org/) more efficiently. 

It is designed for Linux systems (Debian, WSL, ...)



### Why?

While [soroban-cli](https://soroban.stellar.org/docs/reference/soroban-cli) is like a Swiss knife to interact with Soroban, it also requires many arguments and parameters to specify the context, such as the current network being used, the last deployment addresses, ...

The idea behind `sorodev` is to bring tools on top of `soroban-cli` . It can be used to:

- create new Soroban projects and contracts (create default `Cargo.toml`, `lib.rs`, `test.rs`)
- use a `sorodev.json` to configure the current parameters
- build, test, deploy, fund account and make contract bindings with simple commands



To sum up, you can think of it as an equivalent of Hardhat for Soroban.



# Getting started

## Installation

### Install Soroban

Install Rust

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Install the WebAssembly compilation target

```
rustup target add wasm32-unknown-unknown
```

Install `soroban-cli`

```
cargo install soroban-cli
```



### Install Sorodev

```shell
pip install sorodev
```



## Standalone project

```shell
sorodev install-app example
cd example
sorodev add-contract other_contract
sorodev build
sorodev test
sorodev deploy
sorodev make-binding example
sorodev invoke hello --args "--to Sorodev"
```



## Create an Astro project

```shell
npm create astro@4.0.1 example --\
	--template basics\
	--install\ 
	--no-git\
	--typescript strictest
	
sorodev install-app example-astro
cd example-astro
sorodev build
sorodev deploy
sorodev make-binding example-astro
```



In `pages/index.astro`, add the following lines:

```jsx
---
import Layout from "../layouts/Layout.astro";
import Card from "../components/Card.astro";

+ import { Contract, networks } from "example2-client";

+ const greeter = new Contract({
+   ...networks.testnet,
+   rpcUrl: "https://soroban-testnet.stellar.org", // from https://soroban.stellar.org/docs/reference/rpc#public-rpc-providers
+ });
+ 
+ const { result } = await greeter.hello({ to: "Soroban" });
---
```



```jsx
- <h1>Welcome to <span class="text-gradient">Astro</span></h1>
+ <h1><span class="text-gradient">{result.join(" ")}</span></h1>
```



In the `package.json`, add the following script:

```
"scripts": {
    ...
    "postinstall": "sorodev build && sorodev deploy && sorodev make-binding example"
}
```



Then run:

```shell
npm i
npm run dev
```

Under `localhost:4321`, you should see `Hello Sorodev`.



## Create a Next.js project