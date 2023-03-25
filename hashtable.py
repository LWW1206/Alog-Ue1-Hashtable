from stock import Stock
from ascii_plot import plot_stock
import os, json

class HashTable:
    """Class representing a hash table"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.symbol_table: list[Stock | None] = [None for _ in range(size)]
        self.name_table: list[Stock | None] = [None for _ in range(size)]

    def add_stock(self, name: str, wkn: str, symbol: str) -> None:
        """Add a stock to hash table."""
        stock = Stock(name, wkn, symbol)
        symbol_hash = self.hash_code(symbol)
        symbol_index = self.find_index(symbol_hash, self.symbol_table)
        
        name_hash = self.hash_code(name)
        name_index = self.find_index(name_hash, self.name_table)
        
        self.symbol_table[symbol_index] = stock
        print(f"Added {name} ({symbol}) at symbol_list index {symbol_index}")

        self.name_table[name_index] = stock
        print(f"Added {name} ({symbol}) at name_list index {name_index}")

    def find_index(self, hash_code: int, table: list[Stock | None]) -> int:
        """Find an empty index in the hash table."""
        index = hash_code % self.size

        if table[index] is None:
            # empty spot found, return index
            return index

        # collision: use quadratic probing to find an empty spot
        else:
            for i in range(1, self.size):
                new_index = (index + i * i) % self.size
                if table[new_index] is None:
                    # empty spot found, return index
                    return new_index

            # if no more empty slot 
            print("Hash table is full")
        return -1
    
    def search_index(self, hash_code: int, table: list[Stock | None]) -> int:
        """Find an empty index in the hash table."""
        index = hash_code % self.size

        if table[index]:
            # if not empty return index; for search
            return index

        return -1


    def hash_code(self, item: str) -> int:
        """Implement Java hashCode() function
        Calculation used following formular:
        hash_code = s[0]*31(n-1) + s[1]*31(n-2) + ... + s[n]
        Note: Different results compared to Java, because no int overflow
        """
        sum = 0
        counter = 1
        for letter in item:
            val = ord(letter) * (31 ** (len(item) - counter))
            sum += val
            counter += 1
        return sum

    def delete_stock(self, symbol: str | None) -> None:
        """Delete a stock from hash table."""
        if symbol:
            index = self.search(symbol)
            stock = self.symbol_table[index]
            if stock is not None:
                stockname = stock.name
                name_index = self.search(stockname)
                self.name_table[name_index] = None
            self.symbol_table[index] = None
        else:
            print("INFO: You need to provide a stock name e.g 'DEL <name>'")

    def import_stock(self, file_path: str | None, symbol: str | None) -> None:
        """Import stock data from file."""
        if file_path and symbol:
            print(f"IMPORT {file_path} to {symbol}")
            index = self.search(symbol)
            stock = self.symbol_table[index]
            if stock:
                stock.add_data_from_csv(file_path)
        else:
            print("INFO: You need to provide a file path e.g 'IMPORT <path/to/file>'")

    def search(self, input: str | None) -> int:
        """Search a stock from hash table.
        Returns the index as positiv int or -1 (=not found).
        """
        if not input:
            print("INFO: You need to provide a stock name e.g 'SEARCH <SYMBOL>'")
            return -1

        symbol_hash = self.hash_code(input)
        symbol_index = self.search_index(symbol_hash, self.symbol_table)
        symbol_stock = self.symbol_table[symbol_index]

        name_hash = self.hash_code(input)
        name_index = self.search_index(name_hash, self.name_table)
        name_stock = self.name_table[name_index]

        if symbol_stock and symbol_stock.symbol == input:
            print(f"Found {input} in symbol_table at index {symbol_index}")
            if symbol_stock.data:
                newest_data = symbol_stock.data[-1]
                print(f"Newest data for {input}: {newest_data}")
            return symbol_index
        elif name_stock and name_stock.name == input:
            print(f"Found {input} in name_table at index {name_index}")
            if name_stock.data:
                newest_data = name_stock.data[-1]
                print(f"Newest data for {input}: {newest_data}")
            return name_index
        else:
            for i in range(1, self.size):
                new_index = (symbol_index + i * i) % self.size
                new_symbol_stock = self.symbol_table[new_index]
                new_name_stock = self.name_table[new_index]

                if new_symbol_stock and new_symbol_stock.symbol == input:
                    print(f"Found {input} in symbol_table at index {new_index}")
                    if new_symbol_stock.data:
                        newest_data = new_symbol_stock.data[-1]
                        print(f"Newest data for {input}: {newest_data}")
                    return new_index
                elif new_name_stock and new_name_stock.name == input:
                    print(f"Found {input} in name_table at index {new_index}")
                    if new_name_stock.data:
                        newest_data = new_name_stock.data[-1]
                        print(f"Newest data for {input}: {newest_data}")
                    return new_index
        return -1

    def plot(self, symbol: str | None) -> None:
        """Plot a stock."""
        if not symbol:
            print("INFO: You need to provide a stock symbol e.g 'PLOT <SYMBOL>'")
            return

        symbol_index = self.search(symbol)
        stock = self.symbol_table[symbol_index]

        if not stock:
            return
        
        if not stock.data:
            return
        
        plot_stock(stock)

    def save(self, filename: str | None) -> None:
        """Save hash table to JSON file."""
        data = dict()

        if not filename:
            print("INFO: You need to provide a file name e.g 'SAVE <FILENAME>'")
            return
        
        data1 = dict()
        cnt1 = 0
        for i in self.symbol_table:
            if i and isinstance(i, Stock):
                data1[cnt1] = {
                    "name": i.name,
                    "wkn": i.wkn,
                    "symbol": i.symbol,
                    "data": i.data,
                }
            cnt1 += 1
        data["symbol_table"] = data1

        data2 = dict()
        cnt2 = 0
        for i in self.name_table:
            if i and isinstance(i, Stock):
                data2[cnt2] = {
                    "name": i.name,
                    "wkn": i.wkn,
                    "symbol": i.symbol,
                    "data": i.data,
                }
            cnt2 += 1
        data["name_table"] = data2

        with open(os.getcwd() + f"/{filename}.json", "w") as outfile:
            json.dump(data, outfile)

    def load(self, filename: str | None) -> None:
        """Load hash table from JSON file."""
        if not filename:
            print("INFO: You need to provide a file name e.g 'LOAD <FILENAME>'")
            return
        
        with open(os.getcwd() + f"/{filename}.json", "r") as infile:
            data = json.load(infile)

            for index, stock_data in data["symbol_table"].items():
                stock = Stock(**stock_data)
                self.symbol_table[int(index)] = stock
            
            for index, stock_data in data["name_table"].items():
                stock = Stock(**stock_data)
                self.name_table[int(index)] = stock
            

    def print_table(self) -> None:
        cnt, cnt2 = 0, 0
        header = "| Hashtable |"
        print(f"{header:=^30}")
        
        print("Symbol_table:")
        for i in self.symbol_table:
            if i:
                print(cnt, i.symbol)
            cnt += 1

        print("Name_table:")
        for j in self.name_table:
            if j:
                print(cnt2, j.name)
            cnt2 += 1
        print()