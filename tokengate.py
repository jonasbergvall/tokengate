import streamlit as st
from wallet_connect import wallet_connect

# Button to connect wallet
wallet_address = wallet_connect(label="wallet", key="wallet")

# Display the connected wallet address
if wallet_address:
    st.write(f"Connected wallet address: {wallet_address}")
else:
    st.write("No wallet connected.")
