import streamlit as st
from web3 import Web3
from streamlit_javascript import st_javascript

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

# Initialize Streamlit app
st.title("TokenGate App")
st.markdown("Check your wallet for supported tokens.")

# Updated MetaMask detection JavaScript
check_metamask_js = """
async function checkMetaMask() {
    try {
        if (window.ethereum) {
            // Check if we can access ethereum object
            const chainId = await window.ethereum.request({ method: 'eth_chainId' });
            return true;
        }
        return false;
    } catch (error) {
        console.error('MetaMask check error:', error);
        return false;
    }
}
await checkMetaMask();
"""

# Updated MetaMask connection JavaScript
connect_metamask_js = """
async function connectMetaMask() {
    try {
        if (window.ethereum) {
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            if (accounts && accounts.length > 0) {
                return accounts[0];
            }
        }
        return null;
    } catch (error) {
        console.error('MetaMask connection error:', error);
        return null;
    }
}
await connectMetaMask();
"""

# Session state initialization
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None
if "metamask_checked" not in st.session_state:
    st.session_state.metamask_checked = False

# Handle wallet connection
if not st.session_state.wallet_address:
    st.markdown("### Connect Your Wallet")
    
    # Add a button to check for MetaMask
    if not st.session_state.metamask_checked:
        if st.button("Check for MetaMask"):
            metamask_available = st_javascript(check_metamask_js)
            st.session_state.metamask_checked = True
            st.session_state.metamask_available = metamask_available
            st.rerun()
    
    # If MetaMask check has been performed
    if st.session_state.metamask_checked:
        if st.session_state.get('metamask_available', False):
            if st.button("Connect MetaMask"):
                wallet_address = st_javascript(connect_metamask_js)
                if wallet_address:
                    st.session_state.wallet_address = wallet_address
                    st.rerun()
                else:
                    st.error("Failed to connect to MetaMask. Please try again.")
        else:
            st.error("MetaMask is not detected. Please install MetaMask to continue.")
            st.markdown("[Install MetaMask](https://metamask.io/download/)")

# Rest of the code (token checking and display) remains the same
if st.session_state.wallet_address:
    st.success(f"Wallet connected: {st.session_state.wallet_address}")
    
    if st.button("Disconnect Wallet"):
        st.session_state.wallet_address = None
        st.session_state.metamask_checked = False  # Reset the check
        st.rerun()
    
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
            except Exception:
                pass
        
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
        st.error(f"Error validating wallet: {e}")
