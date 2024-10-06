import csv
import pickle

def open_file(filename: str) -> list:
    """
    Purpose: Opens a CSV file and extracts the data
    Parameters:filename: str - the name of the file to open, including the .csv suffix.
    returns: list -the raw data extracted from the CSV file as a list of lists
    """
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            raw_data = []
            for i, row in enumerate(reader):
                if i >= 4:  # Skip the first 4 rows
                    raw_data.append([int(x) if x.isdigit() else x for x in row])
            return raw_data
    except (FileNotFoundError, IOError):
        print("That filename is invalid")
        return None

def create_names_dict(raw_data: list, dictionary: dict) -> dict:
    """
    Purpose: Creates a dictionary of names from raw data.
    Parameters: raw_data: list - The raw data extracted from the CSV file
    dictionary: dict - An empty dictionary to populate with names.
    Returns:dict -a dictionary with names as keys and a list of lists containing frequency, gender, and year as values
    """
    for row in raw_data:
        rank, name, frequency, gender, year = row
        if name not in dictionary:
            dictionary[name] = []
        dictionary[name].append([frequency, gender, year])
    return dictionary

def create_top_ten_dict(raw_data: list, dictionary: dict) -> dict:
    """
    purpose: Creates a dictionary of top ten names from raw data.
    Parameters:raw_data: list - The raw data extracted from the CSV file
    dictionary: dict - An empty dictionary to populate with top ten names
    returns:dict-A dictionary with years as keys and a list of lists containing rank, name, frequency, and gender as values
    """
    yearly_names = {}
    for row in raw_data:
        rank, name, frequency, gender, year = row
        if year not in yearly_names:
            yearly_names[year] = []
        yearly_names[year].append([rank, name, frequency, gender])
    
    for year, names in yearly_names.items():
        names.sort()
        top_ten = names[:10] + [name for name in names if name[0] > 10][:10]
        dictionary[year] = top_ten
    
    return dictionary

def load_file(filename: str, names_dict: dict, top_ten_dict: dict) -> (dict, dict): # type: ignore
    """
    Purpose: Loads the raw data and processes it into dictionaries.
    Parameters:filename: str - The default filename to open if no filename is provided.
    names_dict: dict - An empty dictionary to populate with names.
    top_ten_dict: dict - An empty dictionary to populate with top ten names.
    Returns:tuple-a tuple containing the names dictionary and the top ten dictionary.
    """
    try:
        user_filename = input(f"Enter a file name [{filename}]: ") or filename
        raw_data = open_file(user_filename)
        if raw_data:
            names_dict = create_names_dict(raw_data, names_dict)
            top_ten_dict = create_top_ten_dict(raw_data, top_ten_dict)
        return names_dict, top_ten_dict
    except Exception as e:
        print(f"Error loading file: {e}")
        return names_dict, top_ten_dict

def pickle_dicts(filename: str, names_dict: dict, top_ten_dict: dict) -> None:
    """
    purpose: pickles (saves) the dictionaries to a file
    Parameters:filename: str - The default filename to use for saving the dictionaries.
    names_dict: dict - The dictionary of names to save.
    top_ten_dict: dict - The dictionary of top ten names to save. 
    returns: None
    """
    try:
        user_filename = input(f"Enter a file name [{filename}]: ") or filename
        with open(user_filename, 'wb') as f:
            pickle.dump((names_dict, top_ten_dict), f)
    except Exception as e:
        print(f"Error saving file: {e}")

def load_pickle(filename: str) -> (dict, dict): # type: ignore
    """
    purpose: loads the pickled dictionaries from a file
    Parameters:filename: str - The default filename to use for loading the dictionaries.
    returns:tuple- a tuple containing the loaded names dictionary and top ten dictionary
    """
    try:
        user_filename = input(f"Enter a file name [{filename}]: ") or filename
        with open(user_filename, 'rb') as f:
            names_dict, top_ten_dict = pickle.load(f)
            return names_dict, top_ten_dict
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return {}, {}

def name_search(names_dict: dict) -> None:
    """
    purpose: searches for a name in the dictionary and prints the frequencies
    parameters:names_dict: dict - The dictionary of names to search
    returns:none
    """
    name = input("Enter a name: ").capitalize()
    if name in names_dict:
        for entry in names_dict[name]:
            print(f"{entry[2]}: {entry[0]} {entry[1]}")
    else:
        print(f"There were no babies named {name} born in Alberta between 1980 and 2021")

def main() -> None:
    """
    purpose: Displays the menu and processes user commands.
    parameters:None
    returns:none
    """
    names_dict = {}
    top_ten_dict = {}
    while True:
        print("Alberta Baby names")
        print("-------------------------------")
        print("(0) Quit")
        print("(1) Load and process spreadsheet file")
        print("(2) Save processed data")
        print("(3) Open processed data")
        print("(4) Search for a name")
        
        command = input("Enter command: ")
        if command == '0':
            print("Goodbye")
            break
        elif command == '1':
            names_dict, top_ten_dict = load_file("baby-names-frequency_1980_2021.csv", names_dict, top_ten_dict)
        elif command == '2':
            if not names_dict or not top_ten_dict:
                print("There are no data")
            else:
                pickle_dicts("baby_names.pkl", names_dict, top_ten_dict)
        elif command == '3':
            names_dict, top_ten_dict = load_pickle("baby_names.pkl")
            if not names_dict or not top_ten_dict:
                print("Could not load pickle from filename.")
        elif command == '4':
            if not names_dict:
                print("There are no data")
            else:
                name_search(names_dict)
        else:
            print("Invalid command, please try again")

if __name__ == "__main__":
    main()

