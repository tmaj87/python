import random
import time
from flask import Flask, jsonify
import threading

class StockPriceSimulator:
    def __init__(self, initial_price: float, shares_outstanding: int):
        self.current_price = initial_price
        self.previous_price = initial_price
        self.shares_outstanding = shares_outstanding
        self.price_history = [(time.time(), initial_price)]

    def update_price(self):
        """Updates the stock price based on random buy or sell activity."""
        if random.random() < 0.5:  # 50% chance to buy or sell shares
            shares = random.randint(1_000, 10_000)
            if random.random() < 0.5:
                self.buy_shares(shares)
            else:
                self.sell_shares(shares)

    def calculate_velocity(self):
        """Calculates the velocity of price change based on the last 15 seconds."""
        current_time = time.time()
        recent_prices = [(t, p) for t, p in self.price_history if current_time - t <= 15]

        if len(recent_prices) < 2:
            return 0.0  # Not enough data to calculate velocity

        oldest_time, oldest_price = recent_prices[0]
        newest_time, newest_price = recent_prices[-1]

        time_difference = newest_time - oldest_time
        price_difference = newest_price - oldest_price

        if time_difference == 0:
            return 0.0

        velocity = price_difference / time_difference
        return velocity

    def calculate_market_cap(self):
        """Calculates the market capitalization."""
        return self.current_price * self.shares_outstanding

    def calculate_candle(self, interval: int = 60):
        """Calculates the candle data (open, high, low, close) for a given interval."""
        current_time = time.time()
        interval_prices = [p for t, p in self.price_history if current_time - t <= interval]

        if not interval_prices:
            return None  # No data for the interval

        open_price = interval_prices[0]
        close_price = interval_prices[-1]
        high_price = max(interval_prices)
        low_price = min(interval_prices)

        return {
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price
        }

    def buy_shares(self, number_of_shares: int):
        """Buys a specified number of shares and increases the price."""
        total_cost = number_of_shares * self.current_price
        self.shares_outstanding += number_of_shares
        self.previous_price = self.current_price
        self.current_price += number_of_shares * 0.0001  # Increase price based on shares bought
        self.price_history.append((time.time(), self.current_price))
        print(f"Bought {number_of_shares} shares for ${total_cost:.2f}. Total shares outstanding: {self.shares_outstanding}")

    def sell_shares(self, number_of_shares: int):
        """Sells a specified number of shares and decreases the price."""
        number_of_shares = min(number_of_shares, self.shares_outstanding)  # Ensure shares to sell do not exceed available
        total_revenue = number_of_shares * self.current_price
        self.shares_outstanding -= number_of_shares
        self.previous_price = self.current_price
        self.current_price -= number_of_shares * 0.0001  # Decrease price based on shares sold
        self.current_price = max(self.current_price, 0.01)  # Ensure price does not drop below 0.01
        self.price_history.append((time.time(), self.current_price))
        print(f"Sold {number_of_shares} shares for ${total_revenue:.2f}. Total shares outstanding: {self.shares_outstanding}")

    def simulate(self):
        """Runs the simulation indefinitely."""
        while True:
            self.update_price()
            time.sleep(1)

# Flask app to expose the simulator's data
app = Flask(__name__)
simulator = StockPriceSimulator(initial_price=100.0, shares_outstanding=1_000_000)

def run_simulator():
    simulator.simulate()

@app.route("/current_price", methods=["GET"])
def get_current_price():
    return jsonify({"current_price": simulator.current_price})

@app.route("/velocity", methods=["GET"])
def get_velocity():
    velocity = simulator.calculate_velocity()
    return jsonify({"velocity": velocity})

@app.route("/market_cap", methods=["GET"])
def get_market_cap():
    market_cap = simulator.calculate_market_cap()
    return jsonify({"market_cap": market_cap})

@app.route("/candle", methods=["GET"])
def get_candle():
    candle = simulator.calculate_candle()
    return jsonify(candle if candle else {"error": "No candle data available"})

if __name__ == "__main__":
    threading.Thread(target=run_simulator, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
