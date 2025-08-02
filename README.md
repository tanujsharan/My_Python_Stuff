# Zerodha Kite Connect Integration for Cursor

This project provides a complete integration setup for connecting your Zerodha trading account with Cursor IDE for algorithmic trading in Indian markets.

## 🚀 Features

- **Easy Authentication**: Streamlined login process with token management
- **Comprehensive Trading Interface**: High-level API for placing orders, managing positions, and retrieving market data
- **Real-time Market Data**: Access to live quotes, historical data, and market instruments
- **Portfolio Management**: Track holdings, positions, and P&L
- **Safety First**: Built-in safeguards and examples with safety measures
- **Pandas Integration**: Easy data analysis with DataFrames

## 📋 Prerequisites

1. **Zerodha Trading Account**: You need an active Zerodha trading account
2. **Kite Connect Developer Account**: Register at [developers.kite.trade](https://developers.kite.trade/signup)
3. **Python 3.7+**: Make sure you have Python installed
4. **API Credentials**: API Key and Secret from your developer account

## 🛠️ Setup Instructions

### Step 1: Clone and Setup Environment

```bash
# Navigate to your project directory
cd /workspace

# Create a virtual environment (if not using system packages)
python3 -m venv zerodha_env
source zerodha_env/bin/activate  # On Windows: zerodha_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Zerodha API Credentials

1. **Create a Zerodha Account**: If you don't have one, create an account at [zerodha.com](https://zerodha.com)

2. **Register for Kite Connect**:
   - Visit [developers.kite.trade/signup](https://developers.kite.trade/signup)
   - Create a developer account
   - Create a new "Connect App"
   - Note down your **API Key** and **API Secret**

3. **Configure Environment Variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your credentials
   nano .env  # or use any text editor
   ```

   Update the `.env` file:
   ```env
   ZERODHA_API_KEY=your_actual_api_key_here
   ZERODHA_API_SECRET=your_actual_api_secret_here
   ZERODHA_ACCESS_TOKEN=your_access_token_here
   DEBUG=False
   ```

### Step 3: First-Time Authentication

```bash
# Run the authentication script
python zerodha_auth.py
```

This will:
1. Open your browser to the Zerodha login page
2. Guide you through the login process
3. Extract and save your access token
4. Verify the connection

## 📖 Usage Examples

### Basic Authentication and Account Info

```python
from zerodha_auth import ZerodhaAuth
from zerodha_trading import ZerodhaTrader

# Initialize and authenticate
trader = ZerodhaTrader()

# Get account summary
trader.display_account_summary()

# Get margins
margins = trader.get_margins()
print(f"Available cash: ₹{margins['available']['cash']:,.2f}")
```

### Market Data

```python
# Search for instruments
infy_instruments = trader.search_instruments("INFY", "NSE")
print(infy_instruments[0])

# Get real-time quotes
quote = trader.get_quote("NSE:INFY", "NSE:TCS")
print(f"INFY Price: ₹{quote['NSE:INFY']['last_price']}")

# Get historical data
historical = trader.get_historical_data(
    instrument_token="408065",  # INFY token
    from_date="2024-01-01", 
    to_date="2024-01-31",
    interval="day"
)
```

### Order Management

```python
# Place a market order
order_id = trader.place_market_order(
    symbol="INFY",
    exchange="NSE",
    transaction_type="BUY",
    quantity=1,
    product="CNC"
)

# Place a limit order
order_id = trader.place_limit_order(
    symbol="INFY",
    exchange="NSE", 
    transaction_type="BUY",
    quantity=1,
    price=1500.0,
    product="CNC"
)

# Cancel an order
trader.cancel_order(order_id)

# Get all orders
orders = trader.get_orders()
orders_df = trader.get_orders_df()  # As pandas DataFrame
```

### Portfolio Management

```python
# Get positions
day_positions, net_positions = trader.get_positions_df()
print(net_positions)

# Get holdings
holdings_df = trader.get_holdings_df()
print(holdings_df)

# Calculate portfolio value
portfolio = trader.calculate_portfolio_value()
print(f"Total portfolio value: ₹{portfolio['total_value']:,.2f}")
```

## 🎯 Example Scripts

### Run the Basic Trading Example

```bash
python examples/basic_trading_example.py
```

This example demonstrates:
- Authentication
- Account summary
- Market data retrieval
- Position monitoring
- Order history (safe examples only)

## 📁 Project Structure

```
/workspace/
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # Your actual environment variables (create this)
├── zerodha_auth.py          # Authentication module
├── zerodha_trading.py       # Trading interface module
├── examples/
│   └── basic_trading_example.py  # Basic usage example
└── README.md               # This file
```

## 🔒 Security & Safety

### Important Safety Measures

1. **Never commit your .env file** to version control
2. **Start with small quantities** when testing orders
3. **Use paper trading** or test environment when available
4. **Review all orders** before execution
5. **Set appropriate stop-losses** for risk management

### Environment Security

```bash
# Add .env to your .gitignore
echo ".env" >> .gitignore

# Verify your API keys are not in your code
grep -r "your_api_key" . --exclude-dir=.git
```

## 🔧 Configuration Options

### Order Types

- **MARKET**: Execute immediately at market price
- **LIMIT**: Execute only at specified price or better
- **SL** (Stop Loss): Trigger order when price hits stop price
- **SL-M** (Stop Loss Market): Market order triggered at stop price

### Product Types

- **CNC** (Cash and Carry): For equity delivery trades
- **MIS** (Margin Intraday Square-off): For intraday trades
- **NRML** (Normal): For futures and options
- **CO** (Cover Order): For stop-loss orders
- **BO** (Bracket Order): For target and stop-loss orders

### Exchanges

- **NSE**: National Stock Exchange
- **BSE**: Bombay Stock Exchange  
- **NFO**: NSE Futures and Options
- **BFO**: BSE Futures and Options
- **MCX**: Multi Commodity Exchange
- **CDS**: Currency Derivatives

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**:
   ```bash
   # Check your API credentials
   python -c "from zerodha_auth import ZerodhaAuth; auth = ZerodhaAuth(); print('Credentials OK')"
   ```

2. **Import Errors**:
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Token Expiry**:
   ```bash
   # Re-authenticate if your token has expired
   python zerodha_auth.py
   ```

4. **Network Issues**:
   - Check your internet connection
   - Verify Zerodha's API status
   - Try increasing timeout values

### Debug Mode

Enable debug mode in your `.env` file:
```env
DEBUG=True
```

This will show detailed API request/response information.

## 📚 API Reference

### Key Classes

- **`ZerodhaAuth`**: Handles authentication and token management
- **`ZerodhaTrader`**: High-level trading interface

### Key Methods

- **Authentication**: `get_authenticated_kite()`, `interactive_login()`
- **Orders**: `place_order()`, `cancel_order()`, `modify_order()`
- **Market Data**: `get_quote()`, `get_historical_data()`, `search_instruments()`
- **Portfolio**: `get_positions()`, `get_holdings()`, `calculate_portfolio_value()`

## 📖 Additional Resources

- [Kite Connect API Documentation](https://kite.trade/docs/connect/v3/)
- [PyKiteConnect GitHub](https://github.com/zerodha/pykiteconnect)
- [Zerodha Support](https://support.zerodha.com/)
- [Zerodha Developer Forum](https://kite.trade/forum/)

## ⚠️ Disclaimer

**This software is for educational and informational purposes only. Trading in financial markets involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. Please consult with a financial advisor before making any investment decisions.**

**The authors are not responsible for any financial losses incurred through the use of this software.**

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Happy Trading! 🚀📈**

*Remember: The best trade is the one you don't lose money on.*