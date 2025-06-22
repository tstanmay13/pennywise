# Pennywise

A personal finance management application powered by Plaid API.

## Description

Pennywise is a minimal Mint-style personal finance tracker built with Python and Flask. It integrates with Plaid's sandbox environment to pull transaction data from connected bank accounts.

## Features

- Connect bank accounts via Plaid Link
- View recent transactions
- Clean, modern web interface
- Real-time transaction data
- Secure API integration

## Prerequisites

- Python 3.8 or higher
- Plaid account with API credentials

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tstanmay13/pennywise.git
   cd pennywise
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   py -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Edit the `.env` file with your Plaid credentials:
   ```
   PLAID_CLIENT_ID=your_plaid_client_id
   PLAID_SECRET=your_plaid_sandbox_secret
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

## Running the Application

### Option 1: Using the run script (Windows)
```bash
run.bat
```

### Option 2: Using the run script (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual activation
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Click "Connect Bank Account"** to link your bank via Plaid
3. **Use Plaid's sandbox credentials** for testing:
   - Username: `user_good`
   - Password: `pass_good`
4. **Click "Get Transactions"** to view your recent transactions

## API Endpoints

- `GET /` - Main application interface
- `POST /create_link_token` - Create Plaid Link token
- `POST /exchange_public_token` - Exchange public token for access token
- `POST /get_transactions` - Retrieve transaction data

## Project Structure

```
pennywise/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── run.bat              # Windows run script
├── run.sh               # Unix run script
├── .gitignore           # Git ignore rules
├── templates/
│   └── index.html       # Main web interface
└── static/
    ├── css/             # Stylesheets
    └── js/              # JavaScript files
```

## Development

This application uses:
- **Flask** - Web framework
- **Plaid Python SDK** - Banking API integration
- **python-dotenv** - Environment variable management

## Security Notes

- Never commit your `.env` file to version control
- Use Plaid's sandbox environment for development
- Store production credentials securely

## Troubleshooting

1. **Plaid API errors**: Ensure your credentials are correct and you're using the sandbox environment
2. **Virtual environment issues**: Make sure you've activated the virtual environment before installing dependencies
3. **Port conflicts**: Change the port in `app.py` if port 5000 is already in use

## License

This project is for personal use only. 