from stock import Stock


def rotate_array(array: list[list]) -> list[list]:
    """Rotate given 2D array counter-clockwise."""
    rows = len(array)
    cols = len(array[0])
    # Create new array temporary filled with '0'
    new_array = [[0 for _ in range(rows)] for _ in range(cols)]

    # Fill new array with rotated array data
    for i in range(rows):
        for j in range(cols):
            new_array[cols - j - 1][i] = array[i][j]

    return new_array


def plot_stock(stock: Stock):
    """Plot a stock as an ASCII chart."""
    stock_data = stock.data
    if not stock_data:
        return
    bars = list()
    min_value = min([float(row[4]) for row in stock_data])
    max_value = max([float(row[4]) for row in stock_data]) - min_value
    dates = [row[0] for row in stock_data]

    bars.append(["   |" for _ in range(11)])
    for value in [float(row[4]) for row in stock_data]:
        bar = list()
        val = float(value) - min_value
        height = int((val / max_value) * 10)
        bar.append("#")
        for _ in range(height):
            bar.append("#")
        for _ in range(10 - height):
            bar.append(" ")
        bar.append(" ")
        bars.append(bar)

    arr = rotate_array(bars)

    header = "| PLOT DATA |"
    print(f"{header:=^30}")
    date_start = dates[0]
    date_end = dates[-1]
    name = f"{stock.name} [{stock.symbol}]"
    print(f"Name: {name: >24}")
    print(f"Max.: {max_value + min_value:24.2f}")
    print(f"Min.: {min_value:24.2f}")
    print(f"Date start: {date_start: >18}")
    print(f"Date end: {date_end: >20}")
    print()
    
    print(f"{max_value + min_value:.2f}")
    for row in arr:
        for char in row:
            print(char, end="")
        print()
    print(f"{min_value:.2f}")
