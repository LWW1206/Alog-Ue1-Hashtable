import os
from hashtable import HashTable


def print_menu():
    """Print main menu."""
    print("Please select an option:")
    print("[ADD] - Add a stock <NAME WKN SYMBOL>")
    print("[DEL] - Delete a stock <SYMBOL>")
    print("[IMPORT] - Import csv data from <FILEPATH> to <SYMBOL>")
    print("[SEARCH] - Search stock <SYMBOL> and find current value")
    print("[PLOT] - Create a plot for <SYMBOL> of the last 30 days")
    print("[SAVE] - Save table to file <FILENAME>")
    print("[LOAD] - Load table from file <FILENAME>")
    print("[QUIT] - Close program")


def quit() -> None:
    """Quit the program."""
    exit()


def handle_input(hash_table: HashTable, user_input: str) -> None:
    """Handle user input."""
    input_list = user_input.split(" ")
    if input_list[0].lower() == "add":
        try:
            hash_table.add_stock(*input_list[1:])
        except TypeError:
            print("ERROR: You need to provide a stock data e.g 'ADD <NAME WKN SYMBOL>'")
            return
    elif input_list[0].lower() == "del":
        try:
            hash_table.delete_stock(input_list[1] if len(input_list) > 1 else None)
        except TypeError:
            print("ERROR: You need to provide a stock symbol e.g 'ADD <SYMBOL>'")
            return
    elif input_list[0].lower() == "import":
        hash_table.import_stock(input_list[1], input_list[2])
    elif input_list[0].lower() == "search":
        hash_table.search(input_list[1] if len(input_list) > 1 else None)
    elif input_list[0].lower() == "plot":
        hash_table.plot(input_list[1] if len(input_list) > 1 else None)
    elif input_list[0].lower() == "save":
        hash_table.save(input_list[1] if len(input_list) > 1 else None)
    elif input_list[0].lower() == "load":
        hash_table.load(input_list[1] if len(input_list) > 1 else None)
    elif input_list[0].lower() == "quit":
        quit()
    else:
        print("Unknown command!")


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    ARRAY_SIZE = 2003
    hash_table = HashTable(ARRAY_SIZE)
    while True:
        print()
        hash_table.print_table()
        print_menu()
        user_input = input(">> ")
        clear_screen()
        handle_input(hash_table, user_input)
