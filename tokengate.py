import streamlit as st

# Function to inject JavaScript for MetaMask connection and Web3 integration
def load_metamask_with_web3():
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/web3@1.6.1/dist/web3.min.js"></script>
    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    // Create Web3 instance
                    const web3 = new Web3(window.ethereum);
                    
                    // Request MetaMask accounts
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const account = accounts[0];
                    
                    // Request balance
                    const balance = await web3.eth.getBalance(account);
                    const balanceInEth = web3.utils.fromWei(balance, 'ether');
                    
                    // Update UI with account and balance
                    document.getElementById('metamask-info').textContent =
                        `Connected: ${account} | Balance: ${balanceInEth} ETH`;
                } catch (error) {
                    document.getElementById('metamask-info').textContent = `Error: ${error.message}`;
                }
            } else {
                document.getElementById('metamask-info').textContent = 'MetaMask is not installed!';
            }
        }
    </script>
    <button onclick="connectMetaMask()">Connect MetaMask</button>
    <div id="metamask-info" style="margin-top: 10px;">Not connected</div>
    """, unsafe_allow_html=True)

# Display the app content
st.title("MetaMask Integration with Web3.js")
st.write("""
This Streamlit app allows you to connect your MetaMask wallet and fetch your Ethereum address and balance directly. 
Click the button below to connect.
""")
load_metamask_with_web3()
