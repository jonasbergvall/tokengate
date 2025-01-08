import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components

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

# Create HTML/JS component for MetaMask interaction
metamask_html = """
<div id="metamask-container">
    <button id="connect-button" style="padding: 10px 20px; background-color: #1f1f1f; color: white; border: none; border-radius: 5px; cursor: pointer;">
        Connect MetaMask
    </button>
    <p id="status" style="margin-top: 10px;"></p>
</div>

<script>
document.getElementById('connect-button').addEventListener('click', async () => {
    const statusElement = document.getElementById('status');
    
    try {
        if (typeof window.ethereum !== 'undefined') {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            if (accounts.length > 0) {
                // Send the address back to Streamlit
                window.parent.postMessage({
                    type: 'metamask_connected',
                    address: accounts[0]
                }, '*');
                
                statusElement.textContent = 'Connected: ' + accounts[0];
                statusElement.style.color = 'green';
            }
        } else {
            statusElement.textContent = 'MetaMask not detected. Please install MetaMask.';
            statusElement.style.color = 'red';
        }
    } catch (error) {
        statusElement.textContent = 'Error connecting to MetaMask: ' + error.message;
        statusElement.style.color = 'red';
    }
});

// Listen for account changes
if (typeof window.ethereum !== 'undefined') {
    window.ethereum.on('accountsChanged', function (accounts) {
        window.parent.postMessage({
            type: 'metamask_account_changed',
            address: accounts[0] || null
        }, '*');
    });
}
</script>
"""

# Session state initialization
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None

# Display MetaMask connection component if not connected
if not st.session_state.wallet_address:
    # Use the HTML component
    components.html(metamask_html, height=100)
    
    # Add a manual address input for testing/backup
    st.markdown("### Or enter wallet address manually:")
    manual_address = st.text_input("Enter Ethereum address (0x...)")
    if manual_address and manual_address.startswith("0x"):
        if st.button("Check Address"):
            st.session_state.wallet_address = manual_address
            st.rerun()

# Rest of your token checking code remains the same
if st.session_state.wallet_address:
    st.success(f"Wallet connected: {st.session_state.wallet_address}")
    
    if st.button("Disconnect Wallet"):
        st.session_state.wallet_address = None
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
