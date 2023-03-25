import csv 

class Stock:
    """Class representing a stock."""

    def __init__(self, name: str, wkn: str, symbol: str, data: None | list[list[str | float | int]] = None, index: int | None = None) -> None:
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.data = data

    def add_data_from_csv(self, csv_filename: str) -> None:
        with open(csv_filename, 'r') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
            self.data = data[-30:]

