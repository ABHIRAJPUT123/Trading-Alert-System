# Import library to download stock market data
import yfinance as yf

# Import library to send WhatsApp messages
import pywhatkit


# Create TradingBot class
class TradingBot:

    # Constructor
    def __init__(self, stock_symbol):

        # Store stock symbol inside object
        self.stock_symbol = stock_symbol

    # Download stock data
    def get_data(self):

        data = yf.download(
            self.stock_symbol,
            period="1mo",
            auto_adjust=True
        )

        print("\n===== DATA HEAD =====")
        print(data.head())

        print("\n===== DATA TYPE =====")
        print(type(data))

        print("\n===== CLOSE TYPE =====")
        print(type(data["Close"]))

        close_prices = data["Close"]

        # Convert to normal Python list
        prices = close_prices.squeeze().tolist()

        return prices

    # Calculate RSI
    def calculate_rsi(self, prices):

        gains = []
        losses = []

        for i in range(1, len(prices)):

            change = prices[i] - prices[i - 1]

            if change > 0:
                gains.append(change)

            elif change < 0:
                losses.append(abs(change))

        # Safety checks
        if len(gains) == 0:
            return 0

        if len(losses) == 0:
            return 100

        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    # Generate signal
    def generate_signal(self, rsi):

        if rsi < 30:
            return "BUY"

        elif rsi > 70:
            return "SELL"

        else:
            return "HOLD"

    # Complete workflow
    def send_alert(self, phone_number):

        # Get stock prices
        prices = self.get_data()

        print("\nPrices Downloaded:")
        print(prices)

        # Calculate RSI
        rsi = self.calculate_rsi(prices)

        # Generate signal
        signal = self.generate_signal(rsi)

        # Create message
        message = f"""
Stock: {self.stock_symbol}

RSI: {rsi:.2f}

Signal: {signal}
"""

        print("\n===== FINAL MESSAGE =====")
        print(message)

        # Send WhatsApp message
        pywhatkit.sendwhatmsg_instantly(
            phone_number,
            message,
            wait_time=20
        )


# ==========================
# PROGRAM STARTS HERE
# ==========================

# Create bot object
bot = TradingBot("RELIANCE.NS")

# Run complete workflow
bot.send_alert("+918690963266")