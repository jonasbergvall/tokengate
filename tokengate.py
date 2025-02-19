import streamlit as st
from wallet_connect import wallet_connect
from web3 import Web3
import time

# PulseChain RPC Endpoint
pulsechain_rpc = "https://rpc.pulsechain.com"
web3 = Web3(Web3.HTTPProvider(pulsechain_rpc))

# Token contract details remain the same
tokens = {
    "TEED": {
        "address": "0xA55385633FFFab595E21880Ed7323cFD7D11Cd25",
        "name": "TEED",
        "content_url": "https://drteed.substack.com/",
        "image_url": "https://bestofworlds.se/web3/images/TEED.png",
        "abi": [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function",
            },
        ],
    },
    "WUPIUPU": {
        "address": "0x12B3E0d79c5dFda3FfA55D57C9697bD509dBf7B0",
        "name": "WUPIUPU",
        "content_url": "https://www.lefthouse.art/wupivision",
        "image_url": "https://bestofworlds.se/web3/images/WUPIUPU.png",
        "abi": [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function",
            },
        ],
    },
}

# Initialize session state variables
if "wallet_connected" not in st.session_state:
    st.session_state.wallet_connected = False
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None

# Streamlit app
st.title("Token Gate with Wallet Connect")
st.markdown("Connect your wallet to check for supported tokens.")

# Wallet connection
wallet_address = wallet_connect(label="Connect", key="wallet")

# Update session state if we get a valid address
if wallet_address and wallet_address != "not":
    st.session_state.wallet_connected = True
    st.session_state.wallet_address = wallet_address
elif wallet_address == "not":
    st.session_state.wallet_connected = False
    st.session_state.wallet_address = None

# Check if wallet is connected
if st.session_state.wallet_connected and st.session_state.wallet_address:
    st.success(f"Connected wallet: {st.session_state.wallet_address}")
    st.markdown("You can now interact with the dApp.")

    if st.button("Check Tokens"):
        if st.session_state.wallet_address.startswith("0x") and len(st.session_state.wallet_address) == 42:
            try:
                checksum_address = web3.to_checksum_address(st.session_state.wallet_address)
                detected_tokens = []

                for token_name, token_details in tokens.items():
                    try:
                        token_contract = web3.eth.contract(
                            address=token_details["address"],
                            abi=token_details["abi"]
                        )
                        raw_balance = token_contract.functions.balanceOf(checksum_address).call()
                        decimals = token_contract.functions.decimals().call()

                        balance = raw_balance / (10 ** decimals)
                        if balance > 0:
                            detected_tokens.append(token_details)
                    except Exception as e:
                        st.warning(f"Error checking token {token_name}: {e}")

                if detected_tokens:
                    st.success("The wallet holds the following tokens:")
                    for token in detected_tokens:
                        st.markdown(
                            f"""
                            <div style="display: flex; align-items: center; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
                                <img src="{token['image_url']}" alt="{token['name']}" style="width: 60px; height: 60px; border-radius: 5px; margin-right: 15px;">
                                <div>
                                    <p style="margin: 0; font-size: 16px; font-weight: bold;">Access granted: {token['name']}</p>
                                    <p style="margin: 5px 0 0; font-size: 14px;">Since you hold the {token['name']} token, you have access to exclusive content.</p>
                                    <a href="{token['content_url']}" target="_blank" style="color: #007bff; text-decoration: none;">Access the content</a>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning("The wallet does not hold any supported tokens.")
            except Exception as e:
                st.error(f"Error processing wallet address: {e}")
        else:
            st.error("Invalid wallet address. Please connect a valid Ethereum wallet.")
else:
    st.warning("Please connect your wallet to proceed.")
