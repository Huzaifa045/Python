from BB2 import *
import graphics as gr

def get_name_data(name: str, names_dict: dict) -> tuple:
    """
    Purpose: Get the data for the specified name from the dictionary.
    Parameters:
        name: str - the name to search for
        names_dict: dict - the dictionary containing baby names data
    Returns: tuple - two lists containing the frequency data for boys and girls
    """
    boys_data = []
    girls_data = []
    for year in range(1980, 2021 + 1):
        boys_freq = 0
        girls_freq = 0
        if name in names_dict:
            for entry in names_dict[name]:
                if entry[2] == year:
                    if entry[1] == 'Boy':
                        boys_freq = entry[0]
                    elif entry[1] == 'Girl':
                        girls_freq = entry[0]
        boys_data.append(boys_freq)
        girls_data.append(girls_freq)
    return boys_data, girls_data

def draw_trend_graph(name: str, boys_data: list, girls_data: list):
    """
    Purpose: Draw the trend graph for the given name using graphics.py
    Parameters:
        name: str - the name to be graphed
        boys_data: list - the frequency data for boys
        girls_data: list - the frequency data for girls
    Returns: None
    """
    y_max = max(max(boys_data), max(girls_data)) + 2
    y_max = max(y_max, 10)  # Ensure a minimum y_max for better visibility
    
    win = gr.GraphWin(f"Trend for {name}", 1000, 600)
    win.setCoords(1977.5, -y_max * 0.13, 2023, y_max * 1.2)
    
    # Draw axes
    x_axis = gr.Line(gr.Point(1980, 0), gr.Point(2022, 0))
    x_axis.draw(win)
    y_axis = gr.Line(gr.Point(1980, 0), gr.Point(1980, y_max))
    y_axis.draw(win)
    
    # Draw labels for axes
    for year in range(1980, 2023, 2):
        year_label = gr.Text(gr.Point(year, -y_max * 0.05), str(year))
        year_label.setSize(10)
        year_label.draw(win)
    
    for i in range(0, y_max, max(1, y_max // 10)):
        freq_label = gr.Text(gr.Point(1978.5, i), str(i))
        freq_label.setSize(10)
        freq_label.draw(win)
    
    # Draw title
    title = gr.Text(gr.Point(2000, y_max * 1.1), f"Trend for the name {name}")
    title.setSize(16)
    title.setStyle("bold")
    title.draw(win)
    
    subtitle = gr.Text(gr.Point(2000, y_max * 1.05), "Click anywhere to close window")
    subtitle.setSize(12)
    subtitle.setTextColor("red")
    subtitle.draw(win)
    
    # Draw trend lines
    for data, color in [(boys_data, "blue"), (girls_data, "deeppink")]:
        last_point = None
        for year in range(1980, 2022):
            value = data[year - 1980]
            point = gr.Point(year, value)
            if last_point:
                line = gr.Line(last_point, point)
                line.setFill(color)
                line.setWidth(2)
                line.draw(win)
            last_point = point
    
    # Axis labels
    x_label = gr.Text(gr.Point(2000, -y_max * 0.1), "")
    x_label.setSize(12)
    x_label.draw(win)
    
    y_label = gr.Text(gr.Point(1976, y_max // 2), "")
    y_label.setSize(12)
    y_label.draw(win)
    
    win.getMouse()  # Wait for mouse click to close
    win.close()

def graph_trend(names_dict: dict):
    """
    Purpose: Get the name from the user and draw its trend graph.
    Parameters:
        names_dict: dict - the dictionary containing baby names data
    Returns: None
    """
    name = input("Enter a name to graph its trend: ").capitalize()
    if name in names_dict:
        boys_data, girls_data = get_name_data(name, names_dict)
        draw_trend_graph(name, boys_data, girls_data)
    else:
        print(f"There were no babies named {name} born in Alberta between 1980 and 2021")

def main():
    """
    Purpose: The main function to run the Milestone 3 program.
    Parameters: None
    Returns: None
    """
    names_dict = {}
    top_ten_dict = {}
    while True:
        print("\nAlberta Baby names")
        print("-------------------------------")
        print("(0) Quit")
        print("(1) Load and process spreadsheet file")
        print("(2) Save processed data")
        print("(3) Open processed data")
        print("(4) Search for a name")
        print("(5) Print top ten list for a year")
        print("(6) Search for names with specific letters")
        print("(7) Graphically display the trend of a name")
        
        choice = input("Enter command: ")
        
        if choice == "0":
            print("Goodbye")
            break
        elif choice == "1":
            names_dict, top_ten_dict = load_file("baby-names-frequency_1980_2021.csv", names_dict, top_ten_dict)
        elif choice == "2":
            if not names_dict or not top_ten_dict:
                print("There are no data")
            else:
                pickle_dicts("baby_names.pkl", names_dict, top_ten_dict)
        elif choice == "3":
            result = load_pickle("baby_names.pkl")
            if result:
                names_dict, top_ten_dict = result
            else:
                print("Could not load pickle from baby_names.pkl.")
        elif choice == "4":
            if not names_dict:
                print("There are no data")
            else:
                name_search(names_dict)
        elif choice == "5":
            if not top_ten_dict:
                print("There are no data")
            else:
                print_top_ten(top_ten_dict)
        elif choice == "6":
            if not names_dict:
                print("There are no data")
            else:
                wildcard_search(names_dict)
        elif choice == "7":
            if not names_dict:
                print("There are no data")
            else:
                graph_trend(names_dict)
        else:
            print("Invalid option, please enter a valid number.")

if __name__ == "__main__":
    main()
