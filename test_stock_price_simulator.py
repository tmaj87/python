import unittest
from stock_price_simulator import StockPriceSimulator

class TestStockPriceSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = StockPriceSimulator(initial_price=100.0, shares_outstanding=1_000_000)

    def test_initial_state(self):
        self.assertEqual(self.simulator.current_price, 100.0)
        self.assertEqual(self.simulator.previous_price, 100.0)
        self.assertEqual(self.simulator.shares_outstanding, 1_000_000)
        self.assertEqual(len(self.simulator.price_history), 1)

    def test_buy_shares(self):
        self.simulator.buy_shares(10_000)
        self.assertEqual(self.simulator.shares_outstanding, 1_010_000)
        self.assertGreater(self.simulator.current_price, 100.0)
        self.assertEqual(len(self.simulator.price_history), 2)

    def test_sell_shares(self):
        self.simulator.sell_shares(10_000)
        self.assertEqual(self.simulator.shares_outstanding, 990_000)
        self.assertLess(self.simulator.current_price, 100.0)
        self.assertEqual(len(self.simulator.price_history), 2)

    def test_sell_more_shares_than_available(self):
        self.simulator.sell_shares(2_000_000)  # Attempt to sell more than available
        self.assertEqual(self.simulator.shares_outstanding, 0)
        self.assertGreaterEqual(self.simulator.current_price, 0.01)  # Price should not go below 0.01

    def test_velocity_calculation(self):
        self.simulator.buy_shares(10_000)
        self.simulator.sell_shares(5_000)
        velocity = self.simulator.calculate_velocity()
        self.assertIsInstance(velocity, float)

    def test_market_cap_calculation(self):
        self.simulator.buy_shares(10_000)
        market_cap = self.simulator.calculate_market_cap()
        self.assertAlmostEqual(market_cap, self.simulator.current_price * self.simulator.shares_outstanding)

    def test_candle_calculation(self):
        self.simulator.buy_shares(10_000)
        self.simulator.sell_shares(5_000)
        candle = self.simulator.calculate_candle(interval=60)
        self.assertIsNotNone(candle)
        self.assertIn("open", candle)
        self.assertIn("high", candle)
        self.assertIn("low", candle)
        self.assertIn("close", candle)

if __name__ == "__main__":
    unittest.main()
