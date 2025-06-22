from flask import Flask, request, jsonify, render_template
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import os
from dotenv import load_dotenv
from datetime import datetime, date

# Load environment variables
load_dotenv()

app = Flask(__name__)

# This is a dummy redirect_uri.
# In production, you should have a real endpoint.
# Make sure to add this to your Plaid dashboard under allowed redirect URIs.
REDIRECT_URI = os.getenv('PLAID_REDIRECT_URI', 'http://localhost:5000/')

# Initialize Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    """Create a Plaid Link token for connecting bank accounts"""
    try:
        # Create link token request
        request_data = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="Pennywise",
            country_codes=[CountryCode("US")],
            language="en",
            redirect_uri=REDIRECT_URI,
            user=LinkTokenCreateRequestUser(
                client_user_id="user-id"
            )
        )
        
        # Create link token
        response = client.link_token_create(request_data)
        
        return jsonify({
            "success": True,
            "link_token": response['link_token'],
            "expiration": response['expiration']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/create_link_token_amex', methods=['POST'])
def create_link_token_amex():
    try:
        request_data = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="Pennywise",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(
                client_user_id="user-id"
            ),
            institution_id="ins_amex",
            redirect_uri=REDIRECT_URI
        )
        response = client.link_token_create(request_data)
        return jsonify({
            "success": True,
            "link_token": response['link_token'],
            "expiration": response['expiration']
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    """Get recent transactions using an access token"""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({
                "success": False,
                "error": "access_token is required"
            }), 400
        
        # Use current year for demo
        start_date = date(date.today().year, 1, 1)
        end_date = date.today()
        
        # Create transactions request
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options=TransactionsGetRequestOptions(
                count=100
            )
        )
        
        # Get transactions
        response = client.transactions_get(request_data)
        
        transactions = response['transactions']
        return jsonify({
            "success": True,
            "transactions": [
                {
                    "id": t['transaction_id'],
                    "amount": t['amount'],
                    "date": t['date'],
                    "name": t['name'],
                    "category": t['category'],
                    "account_id": t['account_id']
                }
                for t in transactions
            ],
            "total_transactions": response['total_transactions']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    """Exchange public token for access token"""
    try:
        data = request.get_json()
        public_token = data.get('public_token')
        
        if not public_token:
            return jsonify({
                "success": False,
                "error": "public_token is required"
            }), 400
        
        # Exchange public token for access token
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(exchange_request)
        
        return jsonify({
            "success": True,
            "access_token": response['access_token'],
            "item_id": response['item_id']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 