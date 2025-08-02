"""
Zerodha Trading Interface

This module provides a high-level interface for trading operations
using the Zerodha Kite Connect API.
"""

import pandas as pd
from datetime import datetime, timedelta
from kiteconnect import KiteConnect
from zerodha_auth import ZerodhaAuth


class ZerodhaTrader:
    """
    High-level trading interface for Zerodha Kite Connect API.
    
    Provides methods for placing orders, managing positions, retrieving market data,
    and monitoring account status.
    """
    
    def __init__(self, kite_instance=None):
        """
        Initialize the trading interface.
        
        Args:
            kite_instance (KiteConnect): Authenticated KiteConnect instance
        """
        if kite_instance:
            self.kite = kite_instance
        else:
            # Auto-authenticate
            auth = ZerodhaAuth()
            self.kite = auth.get_authenticated_kite()
            
        if not self.kite:
            raise ValueError("Could not establish authenticated connection to Zerodha")
        
        # Get user profile
        self.user_profile = self.kite.profile()
        print(f"🔗 Connected to Zerodha as: {self.user_profile.get('user_name', 'Unknown')}")
    
    # =============================================================================
    # ACCOUNT & PROFILE METHODS
    # =============================================================================
    
    def get_profile(self):
        """Get user profile information."""
        return self.kite.profile()
    
    def get_margins(self, segment=None):
        """
        Get account margins.
        
        Args:
            segment (str): Trading segment ('equity' or 'commodity')
            
        Returns:
            dict: Margin information
        """
        return self.kite.margins(segment)
    
    def get_positions(self):
        """
        Get current positions.
        
        Returns:
            dict: Positions data with day and net positions
        """
        return self.kite.positions()
    
    def get_holdings(self):
        """
        Get equity holdings.
        
        Returns:
            list: List of holdings
        """
        return self.kite.holdings()
    
    # =============================================================================
    # ORDER MANAGEMENT METHODS
    # =============================================================================
    
    def place_order(self, 
                   symbol, 
                   exchange, 
                   transaction_type, 
                   quantity,
                   order_type="MARKET", 
                   product="CNC",
                   price=None,
                   trigger_price=None,
                   validity="DAY",
                   variety="regular"):
        """
        Place an order.
        
        Args:
            symbol (str): Trading symbol (e.g., "INFY")
            exchange (str): Exchange ("NSE", "BSE", "NFO", "CDS", "BFO", "MCX")
            transaction_type (str): "BUY" or "SELL"
            quantity (int): Quantity to trade
            order_type (str): "MARKET", "LIMIT", "SL", "SL-M"
            product (str): "CNC", "MIS", "NRML", "CO", "BO"
            price (float): Price for limit orders
            trigger_price (float): Trigger price for stop-loss orders
            validity (str): "DAY", "IOC"
            variety (str): "regular", "bo", "co", "amo"
            
        Returns:
            str: Order ID
        """
        try:
            order_id = self.kite.place_order(
                variety=variety,
                exchange=exchange,
                tradingsymbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                product=product,
                order_type=order_type,
                price=price,
                trigger_price=trigger_price,
                validity=validity
            )
            
            print(f"✅ Order placed successfully! Order ID: {order_id}")
            return order_id
            
        except Exception as e:
            print(f"❌ Order placement failed: {e}")
            raise
    
    def place_market_order(self, symbol, exchange, transaction_type, quantity, product="CNC"):
        """
        Place a market order (simplified method).
        
        Args:
            symbol (str): Trading symbol
            exchange (str): Exchange
            transaction_type (str): "BUY" or "SELL"
            quantity (int): Quantity
            product (str): Product type
            
        Returns:
            str: Order ID
        """
        return self.place_order(
            symbol=symbol,
            exchange=exchange,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type="MARKET",
            product=product
        )
    
    def place_limit_order(self, symbol, exchange, transaction_type, quantity, price, product="CNC"):
        """
        Place a limit order (simplified method).
        
        Args:
            symbol (str): Trading symbol
            exchange (str): Exchange
            transaction_type (str): "BUY" or "SELL"
            quantity (int): Quantity
            price (float): Limit price
            product (str): Product type
            
        Returns:
            str: Order ID
        """
        return self.place_order(
            symbol=symbol,
            exchange=exchange,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type="LIMIT",
            price=price,
            product=product
        )
    
    def cancel_order(self, order_id, variety="regular"):
        """
        Cancel an order.
        
        Args:
            order_id (str): Order ID to cancel
            variety (str): Order variety
            
        Returns:
            str: Cancelled order ID
        """
        try:
            cancelled_id = self.kite.cancel_order(variety=variety, order_id=order_id)
            print(f"✅ Order {order_id} cancelled successfully!")
            return cancelled_id
        except Exception as e:
            print(f"❌ Order cancellation failed: {e}")
            raise
    
    def modify_order(self, order_id, variety="regular", **kwargs):
        """
        Modify an existing order.
        
        Args:
            order_id (str): Order ID to modify
            variety (str): Order variety
            **kwargs: Order parameters to modify (quantity, price, etc.)
            
        Returns:
            str: Modified order ID
        """
        try:
            modified_id = self.kite.modify_order(variety=variety, order_id=order_id, **kwargs)
            print(f"✅ Order {order_id} modified successfully!")
            return modified_id
        except Exception as e:
            print(f"❌ Order modification failed: {e}")
            raise
    
    def get_orders(self):
        """
        Get all orders for the day.
        
        Returns:
            list: List of orders
        """
        return self.kite.orders()
    
    def get_order_history(self, order_id):
        """
        Get order history for a specific order.
        
        Args:
            order_id (str): Order ID
            
        Returns:
            list: Order history
        """
        return self.kite.order_history(order_id)
    
    def get_trades(self):
        """
        Get all trades for the day.
        
        Returns:
            list: List of trades
        """
        return self.kite.trades()
    
    # =============================================================================
    # MARKET DATA METHODS
    # =============================================================================
    
    def get_instruments(self, exchange=None):
        """
        Get list of tradeable instruments.
        
        Args:
            exchange (str): Specific exchange (optional)
            
        Returns:
            list: List of instruments
        """
        return self.kite.instruments(exchange)
    
    def search_instruments(self, query, exchange=None):
        """
        Search for instruments by name/symbol.
        
        Args:
            query (str): Search query
            exchange (str): Specific exchange (optional)
            
        Returns:
            list: Matching instruments
        """
        instruments = self.get_instruments(exchange)
        query = query.upper()
        
        matches = []
        for instrument in instruments:
            if (query in instrument['tradingsymbol'].upper() or 
                query in instrument['name'].upper()):
                matches.append(instrument)
        
        return matches
    
    def get_quote(self, *symbols):
        """
        Get quote for instruments.
        
        Args:
            *symbols: Instrument symbols in format "exchange:symbol" (e.g., "NSE:INFY")
            
        Returns:
            dict: Quote data
        """
        return self.kite.quote(list(symbols))
    
    def get_ltp(self, *symbols):
        """
        Get last traded price for instruments.
        
        Args:
            *symbols: Instrument symbols in format "exchange:symbol"
            
        Returns:
            dict: LTP data
        """
        return self.kite.ltp(list(symbols))
    
    def get_ohlc(self, *symbols):
        """
        Get OHLC data for instruments.
        
        Args:
            *symbols: Instrument symbols in format "exchange:symbol"
            
        Returns:
            dict: OHLC data
        """
        return self.kite.ohlc(list(symbols))
    
    def get_historical_data(self, instrument_token, from_date, to_date, interval="day"):
        """
        Get historical data for an instrument.
        
        Args:
            instrument_token (str): Instrument token
            from_date (datetime/str): Start date
            to_date (datetime/str): End date
            interval (str): Candle interval ("minute", "day", "5minute", etc.)
            
        Returns:
            list: Historical candle data
        """
        return self.kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    def get_orders_df(self):
        """
        Get orders as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: Orders DataFrame
        """
        orders = self.get_orders()
        return pd.DataFrame(orders)
    
    def get_positions_df(self):
        """
        Get positions as pandas DataFrames.
        
        Returns:
            tuple: (day_positions_df, net_positions_df)
        """
        positions = self.get_positions()
        day_df = pd.DataFrame(positions['day'])
        net_df = pd.DataFrame(positions['net'])
        return day_df, net_df
    
    def get_holdings_df(self):
        """
        Get holdings as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: Holdings DataFrame
        """
        holdings = self.get_holdings()
        return pd.DataFrame(holdings)
    
    def calculate_portfolio_value(self):
        """
        Calculate total portfolio value.
        
        Returns:
            dict: Portfolio summary
        """
        try:
            holdings = self.get_holdings()
            positions = self.get_positions()
            
            # Calculate holdings value
            holdings_value = sum(
                holding['quantity'] * holding['last_price'] 
                for holding in holdings
            )
            
            # Calculate day positions P&L
            day_pnl = sum(
                position['pnl'] for position in positions['day']
            )
            
            # Calculate net positions P&L
            net_pnl = sum(
                position['pnl'] for position in positions['net']
            )
            
            return {
                'holdings_value': holdings_value,
                'day_pnl': day_pnl,
                'net_pnl': net_pnl,
                'total_value': holdings_value + net_pnl
            }
            
        except Exception as e:
            print(f"❌ Error calculating portfolio value: {e}")
            return None
    
    def display_account_summary(self):
        """Display a comprehensive account summary."""
        print("=" * 60)
        print("📊 ZERODHA ACCOUNT SUMMARY")
        print("=" * 60)
        
        # User info
        profile = self.get_profile()
        print(f"👤 User: {profile.get('user_name', 'Unknown')}")
        print(f"🆔 User ID: {profile.get('user_id', 'Unknown')}")
        print(f"🏢 Broker: {profile.get('broker', 'Unknown')}")
        
        # Margins
        try:
            margins = self.get_margins()
            print(f"\n💰 Available Cash: ₹{margins.get('available', {}).get('cash', 0):,.2f}")
            print(f"💳 Used Margin: ₹{margins.get('utilised', {}).get('debits', 0):,.2f}")
        except Exception as e:
            print(f"⚠️  Could not fetch margins: {e}")
        
        # Portfolio value
        portfolio = self.calculate_portfolio_value()
        if portfolio:
            print(f"\n📈 Holdings Value: ₹{portfolio['holdings_value']:,.2f}")
            print(f"📊 Day P&L: ₹{portfolio['day_pnl']:,.2f}")
            print(f"📊 Net P&L: ₹{portfolio['net_pnl']:,.2f}")
            print(f"💼 Total Portfolio: ₹{portfolio['total_value']:,.2f}")
        
        # Recent orders
        try:
            orders = self.get_orders()
            pending_orders = [o for o in orders if o['status'] == 'OPEN']
            print(f"\n📋 Pending Orders: {len(pending_orders)}")
            print(f"📋 Total Orders Today: {len(orders)}")
        except Exception as e:
            print(f"⚠️  Could not fetch orders: {e}")
        
        print("=" * 60)


def main():
    """
    Example usage of the ZerodhaTrader class.
    """
    try:
        # Initialize trader
        trader = ZerodhaTrader()
        
        # Display account summary
        trader.display_account_summary()
        
        # Example: Search for instruments
        print("\n🔍 Searching for 'INFY' instruments...")
        infy_instruments = trader.search_instruments("INFY", "NSE")
        for instrument in infy_instruments[:3]:  # Show first 3 matches
            print(f"  {instrument['tradingsymbol']} - {instrument['name']}")
        
        # Example: Get quote
        print("\n📊 Getting quote for NSE:INFY...")
        quote = trader.get_quote("NSE:INFY")
        if "NSE:INFY" in quote:
            price = quote["NSE:INFY"]["last_price"]
            print(f"  Last Price: ₹{price}")
        
        # Example: Get recent orders
        print("\n📋 Recent orders:")
        orders_df = trader.get_orders_df()
        if not orders_df.empty:
            print(orders_df[['tradingsymbol', 'transaction_type', 'quantity', 'status', 'order_timestamp']].tail())
        else:
            print("  No orders found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()