import yfinance as yf
from datetime import datetime, timedelta
import sys

class StockSimulator:
    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.portfolio = {}
        self.history = []
        self.current_date = None
        self.data = None
        self.symbol = ""

    def fetch_data(self, symbol, start_date, end_date):
        print(f"Fetching data for {symbol}...")
        stock = yf.Ticker(symbol)
        self.data = stock.history(start=start_date, end=end_date)
        if self.data.empty:
            print("No data found. Please check ticker or date range.")
            return False
        self.symbol = symbol
        self.current_date = self.data.index[0]
        return True

    def next_day(self):
        dates = list(self.data.index)
        if self.current_date not in dates or dates.index(self.current_date) + 1 >= len(dates):
            print("No more data.")
            return False
        self.current_date = dates[dates.index(self.current_date) + 1]
        return True

    def get_price(self):
        if self.current_date in self.data.index:
            return self.data.loc[self.current_date]['Close']
        return None

    def buy(self, shares):
        price = self.get_price()
        total_cost = price * shares
        if total_cost > self.balance:
            print("Not enough balance.")
            return
        self.balance -= total_cost
        self.portfolio[self.symbol] = self.portfolio.get(self.symbol, 0) + shares
        self.history.append((self.current_date.date(), 'BUY', shares, price))
        print(f"Bought {shares} shares at ${price:.2f}")

    def sell(self, shares):
        if self.symbol not in self.portfolio or self.portfolio[self.symbol] < shares:
            print("Not enough shares.")
            return
        price = self.get_price()
        total_gain = price * shares
        self.balance += total_gain
        self.portfolio[self.symbol] -= shares
        self.history.append((self.current_date.date(), 'SELL', shares, price))
        print(f"Sold {shares} shares at ${price:.2f}")

    def portfolio_value(self):
        price = self.get_price()
        shares = self.portfolio.get(self.symbol, 0)
        return shares * price

    def show_status(self):
        price = self.get_price()
        print("\n--- Day Summary ---")
        print(f"Date: {self.current_date.date()}")
        print(f"Price of {self.symbol}: ${price:.2f}")
        print(f"Shares owned: {self.portfolio.get(self.symbol, 0)}")
        print(f"Portfolio Value: ${self.portfolio_value():.2f}")
        print(f"Cash Balance: ${self.balance:.2f}")
        print(f"Net Worth: ${self.balance + self.portfolio_value():.2f}")

def main():
    sim = StockSimulator()

    symbol = input("Enter stock ticker (e.g., AAPL): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    if not sim.fetch_data(symbol, start_date, end_date):
        sys.exit()

    while True:
        sim.show_status()
        action = input("\n[1] Buy  [2] Sell  [3] Next Day  [4] History  [5] Quit\nChoose action: ")

        if action == "1":
            shares = int(input("How many shares to buy? "))
            sim.buy(shares)
        elif action == "2":
            shares = int(input("How many shares to sell? "))
            sim.sell(shares)
        elif action == "3":
            if not sim.next_day():
                break
        elif action == "4":
            for record in sim.history:
                print(record)
        elif action == "5":
            break
        else:
            print("Invalid option.")

    print("\nFinal Portfolio Summary:")
    sim.show_status()

if __name__ == "__main__":
    main()
