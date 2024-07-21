import streamlit as st
from web3 import Web3

# Configuração da conexão com a blockchain (por exemplo, Ganache local)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# ABI do contrato
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "initialSupply",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Endereço do contrato
contract_address = "0x6824074FE1699dC437424f93a023058f99D0C2CE"

# Conectar ao contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Interface Streamlit
st.title("MCAToken Dashboard")

# Conectar com MetaMask
st.markdown("### Conecte-se à sua carteira MetaMask")
user_address = st.text_input("Endereço da Carteira")

# Verificar saldo de tokens
if st.button("Verificar Saldo"):
    balance = contract.functions.balanceOf(user_address).call()
    st.write(f"Saldo de Tokens: {balance}")

# Transferência de tokens
st.markdown("### Transferir Tokens")
to_address = st.text_input("Endereço de Destino")
amount = st.number_input("Quantidade de Tokens", min_value=0)
if st.button("Transferir"):
    tx_hash = contract.functions.transfer(to_address, amount).transact({'from': user_address})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"Transferência de {amount} tokens para {to_address} realizada com sucesso. Tx Hash: {tx_hash.hex()}")

# Aprovar gasto de tokens
st.markdown("### Aprovar Gasto de Tokens")
spender_address = st.text_input("Endereço do Spender")
approve_amount = st.number_input("Quantidade de Tokens para Aprovar", min_value=0)
if st.button("Aprovar"):
    tx_hash = contract.functions.approve(spender_address, approve_amount).transact({'from': user_address})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"Aprovação de {approve_amount} tokens para {spender_address} realizada com sucesso. Tx Hash: {tx_hash.hex()}")

# Verificar Allowance
st.markdown("### Verificar Allowance")
check_spender_address = st.text_input("Endereço do Spender para Verificação")
if st.button("Verificar Allowance"):
    allowance = contract.functions.allowance(user_address, check_spender_address).call()
    st.write(f"Allowance para {check_spender_address}: {allowance}")

# Gastar tokens aprovados
st.markdown("### Gastar Tokens Aprovados")
from_address = st.text_input("Endereço do Owner")
spend_amount = st.number_input("Quantidade de Tokens para Gastar", min_value=0)
if st.button("Gastar"):
    tx_hash = contract.functions.transferFrom(from_address, user_address, spend_amount).transact({'from': user_address})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"Gasto de {spend_amount} tokens do {from_address} para {user_address} realizado com sucesso. Tx Hash: {tx_hash.hex()}")
