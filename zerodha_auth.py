"""
Zerodha Authentication Module

This module handles authentication with Zerodha's Kite Connect API.
It provides methods for login, session management, and token handling.
"""

import os
import hashlib
import webbrowser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Load environment variables
load_dotenv()


class ZerodhaAuth:
    """
    Zerodha Authentication Manager
    
    Handles the complete authentication flow for Zerodha's Kite Connect API.
    """
    
    def __init__(self, api_key=None, api_secret=None, debug=False):
        """
        Initialize the authentication manager.
        
        Args:
            api_key (str): Zerodha API key
            api_secret (str): Zerodha API secret
            debug (bool): Enable debug mode
        """
        self.api_key = api_key or os.getenv('ZERODHA_API_KEY')
        self.api_secret = api_secret or os.getenv('ZERODHA_API_SECRET')
        self.debug = debug or os.getenv('DEBUG', 'False').lower() == 'true'
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API key and secret are required. "
                "Set them in environment variables or pass as parameters."
            )
        
        # Initialize KiteConnect
        self.kite = KiteConnect(api_key=self.api_key, debug=self.debug)
        self.access_token = None
        self.user_profile = None
    
    def get_login_url(self):
        """
        Get the login URL for Zerodha authentication.
        
        Returns:
            str: Login URL
        """
        return self.kite.login_url()
    
    def open_login_page(self):
        """
        Open the Zerodha login page in the default browser.
        """
        login_url = self.get_login_url()
        print(f"Opening Zerodha login page: {login_url}")
        webbrowser.open(login_url)
        return login_url
    
    def authenticate_with_request_token(self, request_token):
        """
        Complete authentication using the request token.
        
        Args:
            request_token (str): Request token from callback URL
            
        Returns:
            dict: Session data including access token
        """
        try:
            # Generate session
            data = self.kite.generate_session(request_token, self.api_secret)
            
            # Store access token
            self.access_token = data["access_token"]
            self.kite.set_access_token(self.access_token)
            
            # Get user profile
            self.user_profile = self.kite.profile()
            
            print(f"✅ Authentication successful!")
            print(f"User: {self.user_profile.get('user_name', 'Unknown')}")
            print(f"User ID: {self.user_profile.get('user_id', 'Unknown')}")
            print(f"Broker: {self.user_profile.get('broker', 'Unknown')}")
            
            return data
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            raise
    
    def extract_request_token_from_url(self, callback_url):
        """
        Extract request token from callback URL.
        
        Args:
            callback_url (str): The callback URL containing request token
            
        Returns:
            str: Request token
        """
        parsed_url = urlparse(callback_url)
        query_params = parse_qs(parsed_url.query)
        
        request_token = query_params.get('request_token')
        if request_token:
            return request_token[0]
        else:
            raise ValueError("Request token not found in callback URL")
    
    def interactive_login(self):
        """
        Interactive login process that guides the user through authentication.
        
        Returns:
            KiteConnect: Authenticated KiteConnect instance
        """
        print("🔐 Starting Zerodha authentication process...")
        print("=" * 50)
        
        # Step 1: Open login page
        login_url = self.open_login_page()
        print(f"\n1. Login URL opened in browser: {login_url}")
        print("   If it didn't open automatically, copy and paste the URL above in your browser.")
        
        # Step 2: Get callback URL
        print("\n2. After logging in, you'll be redirected to a URL.")
        print("   Copy the entire redirect URL and paste it below.")
        callback_url = input("\nPaste the callback URL here: ").strip()
        
        # Step 3: Extract request token
        try:
            request_token = self.extract_request_token_from_url(callback_url)
            print(f"✅ Request token extracted: {request_token[:10]}...")
        except Exception as e:
            print(f"❌ Error extracting request token: {e}")
            return None
        
        # Step 4: Complete authentication
        try:
            session_data = self.authenticate_with_request_token(request_token)
            print(f"\n✅ Access token: {session_data['access_token'][:10]}...")
            print("\nYou can now use the authenticated KiteConnect instance for trading!")
            
            # Save access token to .env file
            self.save_access_token(session_data['access_token'])
            
            return self.kite
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None
    
    def load_existing_token(self):
        """
        Load existing access token from environment.
        
        Returns:
            bool: True if token loaded successfully
        """
        access_token = os.getenv('ZERODHA_ACCESS_TOKEN')
        if access_token and access_token != 'your_access_token_here':
            try:
                self.access_token = access_token
                self.kite.set_access_token(access_token)
                
                # Test the token by getting profile
                self.user_profile = self.kite.profile()
                print(f"✅ Using existing access token for user: {self.user_profile.get('user_name', 'Unknown')}")
                return True
                
            except Exception as e:
                print(f"⚠️  Existing access token is invalid: {e}")
                return False
        
        return False
    
    def save_access_token(self, access_token):
        """
        Save access token to .env file for future use.
        
        Args:
            access_token (str): Access token to save
        """
        try:
            # Read existing .env file
            env_path = '.env'
            env_lines = []
            
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    env_lines = f.readlines()
            
            # Update or add the access token
            token_updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('ZERODHA_ACCESS_TOKEN='):
                    env_lines[i] = f'ZERODHA_ACCESS_TOKEN={access_token}\n'
                    token_updated = True
                    break
            
            if not token_updated:
                env_lines.append(f'ZERODHA_ACCESS_TOKEN={access_token}\n')
            
            # Write back to .env file
            with open(env_path, 'w') as f:
                f.writelines(env_lines)
            
            print(f"💾 Access token saved to .env file")
            
        except Exception as e:
            print(f"⚠️  Could not save access token to .env file: {e}")
    
    def get_authenticated_kite(self):
        """
        Get an authenticated KiteConnect instance.
        
        Returns:
            KiteConnect: Authenticated instance or None if authentication fails
        """
        # Try to load existing token first
        if self.load_existing_token():
            return self.kite
        
        # If no valid token, start interactive login
        print("No valid access token found. Starting authentication process...")
        return self.interactive_login()


def main():
    """
    Main function for testing authentication.
    """
    try:
        # Initialize auth manager
        auth = ZerodhaAuth()
        
        # Get authenticated KiteConnect instance
        kite = auth.get_authenticated_kite()
        
        if kite:
            print("\n🎉 Authentication successful!")
            print("You can now use the 'kite' object for trading operations.")
            
            # Example: Get account margins
            try:
                margins = kite.margins()
                print(f"\n💰 Account margins: {margins}")
            except Exception as e:
                print(f"⚠️  Could not fetch margins: {e}")
        
        else:
            print("❌ Authentication failed!")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()