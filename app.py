import streamlit as st
import requests
import pandas as pd
import os

# Streamlit app title
st.title('Top token trades finder')

body = '''
This app lets you find the largest trades in the last 24h for a particular token, using Dune as a data backend.

[[Query](https://dune.com/queries/3503523)]  |  [[Code](https://github.com/bernatfp/dune-results-demo)]

'''

st.markdown(body, unsafe_allow_html=True)

# Input fields
token_symbol = st.text_input('Token Symbol', 'PEPE')
min_amount = st.number_input('Minimum Amount in USD', min_value=0.0, value=1000.0)

# Submit button
submit = st.button('Submit')

# Handle submission
if submit:
    # Environment variable for the API key
    api_key = os.getenv('DUNE_API_KEY')
    
    # Ensure the API key is set
    if api_key:
        headers = {
            "X-Dune-API-Key": api_key
        }
        
        # Format the API URL
        query = f"(token_bought_symbol = {token_symbol} OR token_sold_symbol = {token_symbol}) AND amount_usd > {min_amount}"
        api_url = f"https://api.dune.com/api/v1/query/3503523/results?filters={query}&columns=token_sold_symbol,token_bought_symbol,amount_usd,address_url,tx_hash_url,tx_from_ens,tx_hash,block_time&sort_by=amount_usd desc&limit=100"
        
        # Send request to the Dune API (tip: you can use our SDK for even easier DX)
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Assuming the API returns a list of trades, convert this to a pandas DataFrame
            df = pd.DataFrame(data['result']['rows'])
            
            # Process DataFrame to display desired columns and format
            df['Action'] = df.apply(lambda row: '📈 BUY' if row['token_bought_symbol'] == token_symbol else '📉 SELL', axis=1)
            df['Amount USD'] = df['amount_usd'].apply(lambda x: f"${x:,.2f}")
            
            # Select and rename columns for display
            df_display = df[['block_time', 'tx_from_ens', 'Action', 'Amount USD', 'tx_hash_url']].rename(columns={
                'token_bought_symbol': 'Token Bought Symbol',
                'token_sold_symbol': 'Token Sold Symbol',
                'tx_hash_url': 'Transaction Hash (Link)',
                'tx_from_ens': 'From'
            })
            
            # Display DataFrame
            st.dataframe(df_display, column_config={
        		"Transaction Hash (Link)": st.column_config.LinkColumn(display_text="View transaction"),
    		})
        else:
            error_message = f'Failed to fetch data. Status code: {response.status_code}. '
            try:
                json_response = response.json()
                if 'message' in json_response:
                    error_message += f'Message: {json_response["message"]}'
                else:
                    error_message += 'Please check your inputs and try again.'
            except ValueError:
                error_message += 'Please check your inputs and try again.'
            st.error(error_message)
    else:
        st.error('API key is not set. Please set the DUNE_API_KEY environment variable.')