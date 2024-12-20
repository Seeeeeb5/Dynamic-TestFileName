"""
Dynamic Test Case Title Builder

This GUI-based tool dynamically creates and formats test case titles by reading data from a CSV file (`data_collection_template_V.csv`). 
The CSV is structured such that each **column** represents each section of the filename, while each **row** contains options for that section. 
The first word in each column acts as the section title, displayed in the GUI, and subsequent words become clickable buttons for users to select and construct their test case titles. 
The final output is a formatted string where sections are separated by default (` - `).

### Features:
1. Dynamic GUI Generation:  
   - The first word in each CSV column serves as a "section title" displayed in the GUI.
   - The remaining words in each column are turned into clickable buttons for title construction.
   - The GUI automatically adapts to any updates made to the CSV (e.g., adding more words or sections).

2. Alt Button Mode:  
   - In "Alt Button" mode, clicking a button appends the word directly to the title string.
   - If "Alt Button" mode is off, the word is inserted into the editable text box for manual adjustments.

3. Section Folders for Grouped Data:  
   - To avoid overwhelming the interface with too many buttons (e.g., for multiple frequencies), the tool supports grouping options into 'folders'.
   - Words in columns without a section title (i.e., empty first row) are treated as sub-options for the preceding titled section. 
   - Check out 'Example excel' further down. The columns next to Freq until Version are all these sub-options relating to the frequencies under the Freq column
   - For example:
     
     'Freq'              'Tests'
      |                     |
      +-- '2.4'             +-- PSD 
      |    |                +-- PWR
      |    +-- 2412         +-- OBW
      |    +-- 2437
      |    +-- 2462
      |
      +-- '5.1'
      |    |
      |    +-- 5180
      |
      +-- 5.7
     
     - In the above example, clicking `2.4` opens a folder allowing the user to choose a specific frequency (e.g., 2412 or 2437).  
     - If a row contains no further sub-options (like 5.7), the button acts normally without opening a folder.

### CSV Format:
- Each column represents a section of the final title.
- The first row in each column is the section's title.
- The remaining rows in that column contain the words users can select for that section.
- If a column lacks a title (empty first row), its words are grouped as sub-options to the left-most titled section.

Example excel:

Tests   Modulation  BW   Freq     -      -      -      Version
PSD     802.11a     20   2.4      2412   2437   2462   1
PWR     802.11n     40   5.1      5180   -      -      FINAL
OBW     -           80   5.7      -      -      -      -


### Instructions:
1. Configure the CSV:  
   - Update the CSV file with the relevant words and sections. The tool will dynamically generate the GUI based on this data.
   - Empty columns will be treated as sub-options (folders) connected to the nearest valid titled column on the left.

2. Run the Script:  
   - Execute the script to open the GUI.
   - Click buttons to select words for your test case title, or manually edit the title using the text box.

3. Output:  
   - The constructed title is displayed in the GUI and printed to the terminal, with sections separated by underscores (`_`).

Integration:
- To integrate this tool into other programs, use the function `run_file_reader()` to retrieve the final constructed test case title as a string.

"""

import tkinter as tk
from datetime import datetime
import csv

def update_buttons():
    """Update buttons and title based on the current row in the transposed data."""
    global current_row_index
    try:
        words = transposed_data[current_row_index]
        clear_buttons()
        
        # Skip empty rows
        while words[0] == '':
            current_row_index += 1
            words = transposed_data[current_row_index]
        
        colstr1.set(words[0])  # Set the section title
        create_word_buttons(words[1:])  # Create buttons for the associated words
        current_row_index += 1
    except IndexError:
        root.quit()  # Close the GUI when all rows have been processed

def handle_subsection(subsection_values, word):
    """Clear current buttons and create buttons for subsection values."""
    clear_buttons()
    colstr1.set(word + " values")
    create_word_buttons(subsection_values)

def insert_word(word):
    """Insert the clicked word into the text box and handle any subsections."""
    global current_row_index
    textbox.delete(0, tk.END)

    # Check if there is a subsection in the next row
    if current_row_index < len(transposed_data):
        next_row = transposed_data[current_row_index]
        
        # If the first element of the next row is empty, it's a subsection
        if next_row[0] == '':
            word_index = transposed_data[current_row_index - 1].index(word)
            subsection_values = []

            # Collect subsection values
            for val in og_data[word_index][current_row_index:]:
                if og_data[0][current_row_index] == '':
                    if val != '':
                        subsection_values.append(val)
                    current_row_index += 1

            # If subsection values exist, handle them and skip normal flow
            if subsection_values:
                handle_subsection(subsection_values, word)
                return
            
    textbox.insert(tk.END, word)

    # If no subsection, continue with normal operation
    if altbuttonFlag.get():
        on_enter()

def on_enter(event=None):
    """Handle the Enter key event, update the displayed text, and load the next row."""
    if textbox.get() != '':
        entered_text.set(f"{entered_text.get()}{connector}{textbox.get()}")
    update_buttons()
    textbox.delete(0, tk.END)

def create_word_buttons(words):
    """Dynamically create buttons for each word in the list."""
    for word in words:
        if word != '':
            button = tk.Button(bFrame, text=word, command=lambda w=word: insert_word(w))
            button.pack(side=tk.LEFT, pady=5, padx=5)
            buttons.append(button)

def clear_buttons():
    """Remove all buttons from the button frame."""
    for btn in buttons:
        btn.destroy()
    buttons.clear()

def read_and_transpose_file(file_name):
    """Read and transpose the CSV file data."""
    global og_data
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        og_data = data
        # Transpose the matrix to handle columns as rows
        transposed = list(map(list, zip(*data)))
        return transposed

def initialize_gui():
    """Set up the main GUI components."""
    root.title("Test Case Title Builder")

    root.minsize(400,150)

    tk.Label(root, textvariable=colstr1, font=('Arial', 12)).pack(side=tk.TOP)
    bFrame.pack(side=tk.TOP)

    textbox.pack(side=tk.LEFT)
    inputFrame.pack(side=tk.TOP)

    result_label.pack(side=tk.TOP)

    # Menu for Alt Button toggle
    buttonmenu = tk.Menu(menuBar, tearoff=0)
    buttonmenu.add_checkbutton(label="Alt Button", variable=altbuttonFlag)
    menuBar.add_cascade(label="Button", menu=buttonmenu)
    root.config(menu=menuBar)

    root.bind('<Return>', on_enter)

def get_time_PC():
    """Return the current PC time as a formatted string."""
    return datetime.now().strftime('%d_%b_%y')
    #return datetime.now().strftime('%d-%b-%Y-%H:%M:%S')

def run_file_reader():
    """Main function to run the file reader and initialize the GUI."""
    global root, colstr1, entered_text, buttons, textbox, result_label, bFrame, inputFrame, menuBar
    global transposed_data, current_row_index, file_name, altbuttonFlag, og_data, connector

    root = tk.Tk()

    colstr1 = tk.StringVar()
    entered_text = tk.StringVar(value=get_time_PC())
    altbuttonFlag = tk.BooleanVar(value=True)
    buttons = []

    textbox = tk.Entry(inputFrame := tk.Frame(root), font=('Arial', 14), justify='center')
    result_label = tk.Label(root, textvariable=entered_text, font=('Arial', 12))
    bFrame = tk.Frame(root)
    menuBar = tk.Menu(root)

    file_name = "data_collection_template_V.csv"
    transposed_data = read_and_transpose_file(file_name)
    current_row_index = 0
    connector = ' - '

    try:
        # Initialize with the first row of transposed data
        first_words = transposed_data[0]
        colstr1.set(first_words[0])
        create_word_buttons(first_words[1:])
    except IndexError:
        colstr1.set("No more lines to read.")
    
    current_row_index += 1

    initialize_gui()
    
    root.mainloop()

    return entered_text.get()

if __name__ == '__main__':
    result = run_file_reader()
    
    print(result)
