import os
import streamlit as st
import streamlit.components.v1 as components

# Write the JavaScript code to a temporary file
def write_javascript_file():
    js_code = """
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
    temp_file_path = os.path.join(os.getcwd(), "metamask_integration.html")
    with open(temp_file_path, "w") as f:
        f.write(js_code)
    return temp_file_path

# Load the JavaScript file
file_path = write_javascript_file()

# Streamlit app layout
st.title("MetaMask Integration with Streamlit")
st.write("""
This app demonstrates connecting a MetaMask wallet to a Streamlit app. 
Click the "Connect MetaMask" button below to retrieve your wallet address and balance.
""")

# Embed the JavaScript via Streamlit custom component
components.html(open(file_path, "r").read(), height=400)

# Clean up (optional)
os.remove(file_path)
