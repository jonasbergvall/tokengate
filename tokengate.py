import streamlit as st
import streamlit.components.v1 as components

# MetaMask integration HTML and JavaScript
metamask_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.jsdelivr.net/npm/web3@1.6.1/dist/web3.min.js"></script>
</head>
<body>
    <button id="connect-button" style="font-size: 16px; padding: 10px;">Connect MetaMask</button>
    <div id="metamask-info" style="margin-top: 10px; font-size: 14px;">Not connected</div>
    <script>
        document.getElementById("connect-button").addEventListener("click", async function() {
            if (typeof window.ethereum !== "undefined") {
                try {
                    const web3 = new Web3(window.ethereum);
                    const accounts = await ethereum.request({ method: "eth_requestAccounts" });
                    const account = accounts[0];
                    const balance = await web3.eth.getBalance(account);
                    const balanceInEth = web3.utils.fromWei(balance, "ether");
                    document.getElementById("metamask-info").textContent =
                        `Connected: ${account} | Balance: ${balanceInEth} ETH`;
                } catch (error) {
                    document.getElementById("metamask-info").textContent = `Error: ${error.message}`;
                }
            } else {
                document.getElementById("metamask-info").textContent = "MetaMask is not installed!";
            }
        });
    </script>
</body>
</html>
"""

# Streamlit app layout
st.title("MetaMask Integration with Streamlit")
st.write("""
This app demonstrates connecting a MetaMask wallet to a Streamlit app. 
Click the "Connect MetaMask" button below to retrieve your wallet address and balance.
""")

# Embed the MetaMask HTML and JavaScript
components.html(metamask_html, height=400)
