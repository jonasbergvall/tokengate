import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("MetaMask Connection Example")

    # Embed HTML and JavaScript (using cdnjs and ethers v6)
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MetaMask Connection</title>
            <script src="https://cdn.jsdelivr.net/npm/ethers@6.0.0/dist/ethers.umd.min.js"></script>
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
                            const provider = new ethers.BrowserProvider(window.ethereum);
                            const signer = await provider.getSigner();
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
    if "connected" in st.session_state and st.session_state.connected:
        st.write(f"Connected account: {st.session_state.address}")
    elif "connected" in st.session_state and not st.session_state.connected:
        st.write(f"Error: {st.session_state.error}")

    def receive_message(message):
        if message and "data" in message and message["data"] and "connected" in message["data"]:
            if message['data']['connected']:
                st.session_state['address'] = message['data']['address']
                st.session_state['connected'] = True
                st.experimental_rerun()
            elif not message['data']['connected']:
                st.session_state['error'] = message['data']['error']
                st.session_state['connected'] = False
                st.experimental_rerun()
        else:
            st.write("Invalid message format received from component.")

    component_value = st.query_params.get('component_value')
    if component_value:
        receive_message(component_value)

    components.html(
        """
        <script>
        window.addEventListener('message', function(event) {
            window.streamlit.setComponentValue(event.data)
        })
        </script>
        """,
        height=0
    )
    st.query_params.clear()

if __name__ == "__main__":
    main()
