import streamlit as st

def load_metamask():
    st.markdown("""
    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    // Request account access
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const account = accounts[0];
                    
                    // Fetch ETH balance
                    const balance = await ethereum.request({
                        method: 'eth_getBalance',
                        params: [account, 'latest']
                    });

                    // Convert balance to ETH
                    const balanceInEth = parseFloat(parseInt(balance, 16) / Math.pow(10, 18)).toFixed(4);

                    // Update the UI
                    const info = `Connected: ${account} | Balance: ${balanceInEth} ETH`;
                    document.getElementById('metamask-info').textContent = info;

                    // Send account and balance back to Streamlit
                    const streamlitData = { account, balanceInEth };
                    Streamlit.setComponentValue(streamlitData);
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

st.title("MetaMask Integration")
load_metamask()
