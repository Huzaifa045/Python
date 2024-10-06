from BB1 import *

def print_top_ten(top_ten_dict):
    """
    purpose:print the top 10 baby names for boys and girls for a given year
    Parameters top_ten_dict: dict  dictionary containing top ten names for each year
    Returns: None
    """
    try:
        year = int(input("Enter year (1980 to 2021): "))
        if 1980 <= year <= 2021:
            if year in top_ten_dict:
                print(f"Top 10 names for baby girls given in Alberta in {year}:")
                if 'Girl' in top_ten_dict[year]:
                    for rank, entry in enumerate(top_ten_dict[year]['Girl'], start=1):
                        print(f"{rank}. {entry[1]}: {entry[2]}")
                else:
                    print(f"No girl names found for the year {year}")

                print(f"\nTop 10 names for baby boys given in Alberta in {year}:")
                if 'Boy' in top_ten_dict[year]:
                    for rank, entry in enumerate(top_ten_dict[year]['Boy'], start=1):
                        print(f"{rank}. {entry[1]}: {entry[2]}")
                else:
                    print(f"No boy names found for the year {year}")
            else:
                print(f"No data available for the year {year}")
        else:
            print("Year out of range, please enter a year between 1980 and 2021.")
    except ValueError:
        print("Invalid input. Please enter a valid year.")
    except KeyError as e:
        print(f"Data structure error: {e}")

def wildcard_search(names_dict):
    """
    Purpose:search for names containing specific letters with a wildcard.
    Parameters:names_dict: dict - Dictionary containing all names
    returns:None
    """
    name_pattern = input("Enter name with * indicating missing letters: ").strip().lower()
    if name_pattern.count('*') != 1:
        print("There must be one and only one asterisk entered")
        return

    parts = name_pattern.split('*')
    prefix, suffix = parts[0], parts[1]

    def match_pattern(name):
        name = name.lower()
        return name.startswith(prefix) and name.endswith(suffix) and len(name) > len(prefix) + len(suffix)

    matches = [name for name in names_dict if match_pattern(name)]

    if not matches:
        print("No names found matching the pattern")
        return

    for match in matches:
        print(f"\n{match.capitalize()}")
        print("  Boys Girls")
        boy_count = 0
        girl_count = 0
        for entry in names_dict[match]:
            if entry[1].lower() == 'boy':
                boy_count += entry[0]
            else:
                girl_count += entry[0]
            print(f"{entry[2]}:  {boy_count}  {girl_count}")

def create_top_ten_dict(raw_data, top_ten_dict):
    """
    purpose: create a dictionary with top ten boys' and girls' names for each year
    Parameters:raw_data: list - Raw data extracted from the CSV file
    top_ten_dict: dict - dictionary to be populated with top ten names.
    returns: dict  dictionary with top ten names for each year
    """
    for row in raw_data:
        year = row[4]
        gender = row[3]
        if year not in top_ten_dict:
            top_ten_dict[year] = {'Boy': [], 'Girl': []}
        if gender == 'Boy' and len(top_ten_dict[year]['Boy']) < 10:
            top_ten_dict[year]['Boy'].append(row[:4])
        elif gender == 'Girl' and len(top_ten_dict[year]['Girl']) < 10:
            top_ten_dict[year]['Girl'].append(row[:4])
    return top_ten_dict

def load_file(filename: str, names_dict, top_ten_dict):
    """
    purpose: Load and process the spreadsheet file.
    Parameters:filename: str - The name of the file to be loaded
    names_dict: dict - Dictionary to be populated with all names
    top_ten_dict: dict - Dictionary to be populated with top ten names
    returns: tuple a tuple containing the populated names_dict and top_ten_dict
    """
    try:
        raw_data = open_file(filename)
        if raw_data:
            print("Raw data loaded successfully.")
            names_dict = create_names_dict(raw_data, names_dict)
            top_ten_dict = create_top_ten_dict(raw_data, top_ten_dict)
            print("Dictionaries created successfully.")
        else:
            print("No raw data to process.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return names_dict, top_ten_dict

def main():
    """
    purpose:main function to run the Alberta Baby Names program
    parameters:none
    Returns:None
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
        print("(5) Print top ten list for a year")
        print("(6) Search for names with specific letters")
        command = input("Enter command: ")
        if command == '0':
            print("Goodbye")
            break
        elif command == '1':
            filename = input("Enter a file name [baby-names-frequency_1980_2021.csv]: ")
            if not filename:
                filename = "baby-names-frequency_1980_2021.csv"
            names_dict, top_ten_dict = load_file(filename, names_dict, top_ten_dict)
        elif command == '2':
            if not names_dict or not top_ten_dict:
                print("There are no data")
            else:
                filename = input("Enter a file name [baby_names.pkl]: ")
                if not filename:
                    filename = "baby_names.pkl"
                pickle_dicts(filename, names_dict, top_ten_dict)
        elif command == '3':
            filename = input("Enter a file name [baby_names.pkl]: ")
            if not filename:
                filename = "baby_names.pkl"
            names_dict, top_ten_dict = load_pickle(filename)
            if not names_dict:
                print("Could not load pickle from", filename)
        elif command == '4':
            if not names_dict:
                print("There are no data")
            else:
                name_search(names_dict)
        elif command == '5':
            if not top_ten_dict:
                print("There are no data")
            else:
                print_top_ten(top_ten_dict)
        elif command == '6':
            if not names_dict:
                print("There are no data")
            else:
                wildcard_search(names_dict)

if __name__ == "__main__":
    main()
