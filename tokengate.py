import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("MetaMask Connection Example")

    # Embed HTML and JavaScript
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MetaMask Connection</title>
            <script src="https://cdn.ethers.io/lib/ethers-5.2.umd.min.js" type="application/javascript"></script>
        </head>
        <body>
            <button id="connectButton">Connect Wallet</button>
            <div id="accountAddress"></div>
            <script>
                const connectButton = document.getElementById('connectButton');
                const accountAddress = document.getElementById('accountAddress');

                connectButton.addEventListener('click', async () => {
                    if (typeof window.ethereum !== 'undefined') {
                        try {
                            await window.ethereum.request({ method: 'eth_requestAccounts' });
                            const provider = new ethers.providers.Web3Provider(window.ethereum);
                            const signer = provider.getSigner();
                            const address = await signer.getAddress();
                            accountAddress.innerText = "Connected Account: " + address;
                            window.parent.postMessage({ 'connected': true, 'address': address }, '*');
                        } catch (error) {
                            console.error("Error connecting:", error);
                            accountAddress.innerText = "Error connecting: " + error.message;
                            window.parent.postMessage({ 'connected': false, 'error': error.message }, '*');
                        }
                    } else {
                        accountAddress.innerText = 'Please install MetaMask!';
                    }
                });
            </script>
        </body>
        </html>
        """,
        height=200,
    )

    # Handle messages from JavaScript
    if "connected" in st.session_state and st.session_state.connected: #check if the key exists before accessing it.
        st.write(f"Connected account: {st.session_state.address}")
    elif "connected" in st.session_state and not st.session_state.connected:
        st.write(f"Error: {st.session_state.error}")

    def receive_message(message):
        if message and "data" in message and message["data"] and "connected" in message["data"]: #check if the keys exists before accessing them.
            if message['data']['connected']:
                st.session_state['address'] = message['data']['address']
                st.session_state['connected'] = True
                st.experimental_rerun()
            elif not message['data']['connected']:
                st.session_state['error'] = message['data']['error']
                st.session_state['connected'] = False
                st.experimental_rerun()
        else:
            st.write("Invalid message format received from component.") #print an error message to help debugging

    # Use st.query_params instead of st.experimental_get_query_params
    component_value = st.query_params.get('component_value')
    if component_value:
        receive_message(component_value)

    components.html(
        f"""
        <script>
        window.addEventListener('message', function(event) {{
            window.streamlit.setComponentValue(event.data)
        }})
        </script>
        """,
        height=0
    )
    st.query_params.clear() #clear the query params.

if __name__ == "__main__":
    main()
