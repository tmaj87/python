import random
import time

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

    def simulate(self, duration: int):
        """Runs the simulation for the specified duration in seconds."""
        start_time = time.time()

        while time.time() - start_time < duration:
            self.update_price()
            velocity = self.calculate_velocity()
            market_cap = self.calculate_market_cap()
            candle = self.calculate_candle()

            print(f"Current Price: ${self.current_price:.2f}")
            print(f"Velocity (change/sec): {velocity:.4f}")
            print(f"Market Cap: ${market_cap:.2f}")

            if candle:
                print(f"Candle (1 min): Open: ${candle['open']:.2f}, High: ${candle['high']:.2f}, Low: ${candle['low']:.2f}, Close: ${candle['close']:.2f}\n")

            time.sleep(1)  # Wait 1 second before the next update

# Usage example
if __name__ == "__main__":
    simulator = StockPriceSimulator(initial_price=100.0, shares_outstanding=1_000_000)
    simulator.simulate(duration=60)  # Simulate for 60 seconds
