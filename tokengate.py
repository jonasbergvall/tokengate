if wallet_address:
    # Ensure the wallet address is valid before using it
    if wallet_address.startswith("0x") and len(wallet_address) == 42:
        try:
            checksum_address = web3.to_checksum_address(wallet_address)

            # Check for tokens in wallet
            detected_tokens = []
            for token_name, token_details in tokens.items():
                try:
                    token_contract = web3.eth.contract(
                        address=token_details["address"], abi=token_details["abi"]
                    )
                    raw_balance = token_contract.functions.balanceOf(checksum_address).call()
                    decimals = token_contract.functions.decimals().call()

                    # Convert balance to human-readable format
                    balance = raw_balance / (10 ** decimals)

                    if balance > 0:
                        detected_tokens.append(token_details)
                except Exception as e:
                    st.warning(f"Error checking token {token_name}: {e}")

            # Display detected tokens
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
    st.warning("No wallet connected. Please connect your wallet to proceed.")
