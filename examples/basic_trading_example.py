#!/usr/bin/env python3
"""
Basic Trading Example with Zerodha

This script demonstrates basic trading operations using the Zerodha integration.
It shows how to:
1. Authenticate with Zerodha
2. Get account information
3. Search for instruments
4. Get market quotes
5. Place orders (commented out for safety)
6. Monitor positions and orders

⚠️  WARNING: This is for educational purposes only.
    Test thoroughly before using real money!
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zerodha_auth import ZerodhaAuth
from zerodha_trading import ZerodhaTrader
import pandas as pd
from datetime import datetime, timedelta


def main():
    """
    Main trading example function.
    """
    print("🚀 Zerodha Basic Trading Example")
    print("=" * 50)
    
    try:
        # Step 1: Initialize trader (this will handle authentication)
        print("🔐 Authenticating with Zerodha...")
        trader = ZerodhaTrader()
        print("✅ Authentication successful!")
        
        # Step 2: Display account summary
        print("\n📊 Account Summary:")
        trader.display_account_summary()
        
        # Step 3: Get available cash and margins
        print("\n💰 Account Margins:")
        margins = trader.get_margins()
        print(f"Available Cash: ₹{margins.get('available', {}).get('cash', 0):,.2f}")
        print(f"Available Margin: ₹{margins.get('available', {}).get('day_utilised', 0):,.2f}")
        
        # Step 4: Search for trading instruments
        print("\n🔍 Searching for instruments...")
        
        # Search for some popular stocks
        symbols_to_search = ["RELIANCE", "TCS", "INFY", "HDFC", "ICICI"]
        
        for symbol in symbols_to_search:
            instruments = trader.search_instruments(symbol, "NSE")
            if instruments:
                inst = instruments[0]  # Get first match
                print(f"  {inst['tradingsymbol']}: {inst['name']}")
        
        # Step 5: Get real-time quotes
        print("\n📈 Real-time Quotes:")
        
        # Popular stock symbols for quotes
        quote_symbols = ["NSE:RELIANCE", "NSE:TCS", "NSE:INFY", "NSE:HDFCBANK", "NSE:ICICIBANK"]
        
        try:
            quotes = trader.get_quote(*quote_symbols)
            
            for symbol in quote_symbols:
                if symbol in quotes:
                    quote = quotes[symbol]
                    price = quote.get('last_price', 0)
                    change = quote.get('net_change', 0)
                    change_pct = quote.get('percentage_change', 0)
                    
                    symbol_name = symbol.split(':')[1]
                    direction = "📈" if change >= 0 else "📉"
                    
                    print(f"  {direction} {symbol_name}: ₹{price:.2f} ({change:+.2f}, {change_pct:+.2f}%)")
                    
        except Exception as e:
            print(f"⚠️  Could not fetch quotes: {e}")
        
        # Step 6: Show current positions
        print("\n📊 Current Positions:")
        try:
            day_positions, net_positions = trader.get_positions_df()
            
            if not net_positions.empty:
                # Show only positions with quantity > 0
                active_positions = net_positions[net_positions['quantity'] != 0]
                
                if not active_positions.empty:
                    print(active_positions[['tradingsymbol', 'quantity', 'average_price', 'last_price', 'pnl']].to_string(index=False))
                else:
                    print("  No active positions")
            else:
                print("  No positions found")
                
        except Exception as e:
            print(f"⚠️  Could not fetch positions: {e}")
        
        # Step 7: Show recent orders
        print("\n📋 Recent Orders (Last 5):")
        try:
            orders_df = trader.get_orders_df()
            
            if not orders_df.empty:
                recent_orders = orders_df.tail(5)
                columns_to_show = ['order_timestamp', 'tradingsymbol', 'transaction_type', 'quantity', 'status', 'average_price']
                
                # Only show columns that exist
                available_columns = [col for col in columns_to_show if col in recent_orders.columns]
                print(recent_orders[available_columns].to_string(index=False))
            else:
                print("  No orders found")
                
        except Exception as e:
            print(f"⚠️  Could not fetch orders: {e}")
        
        # Step 8: Example order placement (COMMENTED OUT FOR SAFETY)
        print("\n⚠️  Order Placement Example (DISABLED FOR SAFETY):")
        print("   Uncomment the code below to place actual orders!")
        print("   Make sure you understand the risks before trading.")
        
        """
        # UNCOMMENT BELOW TO PLACE ACTUAL ORDERS - USE WITH CAUTION!
        
        # Example: Place a small buy order for INFY
        try:
            # Get current price first
            infy_quote = trader.get_ltp("NSE:INFY")
            current_price = infy_quote["NSE:INFY"]["last_price"]
            
            # Place a limit order slightly below current price
            limit_price = current_price * 0.99  # 1% below current price
            
            print(f"\\n📤 Placing BUY order for INFY at ₹{limit_price:.2f}")
            
            order_id = trader.place_limit_order(
                symbol="INFY",
                exchange="NSE", 
                transaction_type="BUY",
                quantity=1,  # Small quantity for testing
                price=limit_price,
                product="CNC"  # Cash and Carry
            )
            
            print(f"✅ Order placed successfully! Order ID: {order_id}")
            
            # You can cancel the order immediately if you want
            # trader.cancel_order(order_id)
            
        except Exception as e:
            print(f"❌ Order placement failed: {e}")
        """
        
        # Step 9: Show portfolio summary
        print("\n💼 Portfolio Summary:")
        portfolio = trader.calculate_portfolio_value()
        if portfolio:
            print(f"  Holdings Value: ₹{portfolio['holdings_value']:,.2f}")
            print(f"  Day P&L: ₹{portfolio['day_pnl']:,.2f}")
            print(f"  Total Portfolio: ₹{portfolio['total_value']:,.2f}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in trading example: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()