"""
A GUI-based tool for dynamically creating and formatting test case titles using data from a CSV file.

This program reads from a CSV file (`data_collection_template.csv`), where each row contains a title (in the first column) 
and a set of associated words (in the subsequent columns). The first word in each row becomes the section title displayed 
in the GUI, while the remaining words are dynamically turned into clickable buttons. Users can select these words to 
build a file name or test case title, which is formatted by separating sections with underscores (_).

### Key Features:
- You can easily update the CSV file by adding new rows or words. Each new row will be processed as a title with associated buttons.
- To add more buttons, simply edit the CSV file by placing words in the row next to the title. 
  These will automatically display as clickable buttons in the GUI.
- If you check the "Save Word?" box in the GUI, any word you type into the text box will be saved back into the 
  CSV file on the current row, ensuring you can modify or append data without editing the file manually if you forget.
- button->AltButton will toggle whether the button press will just put the text into the textbox or automatically put it into the string
  
### How to Use:
- To run the program standalone, simply execute this script. The final test case title will be displayed in the terminal.
- To use the file reader in another program, import `run_file_reader()`. This function will return the final constructed 
  string (i.e., the title) when called.

Note: You cannot use the "Save Word?" feature when the csv is open in the background. It won't crash or anything though so just
close the csv and try again.


"""
import tkinter as tk
from datetime import datetime

def update_buttons():
    """Update the buttons and title based on the next line in the file."""
    global current_row_index
    try:
        words = next(current_line).strip(',\n').split(',')
        clear_buttons()
        colstr1.set(words[0])
        create_word_buttons(words[1:])
        current_row_index += 1
    except StopIteration:
        root.quit()

def read_file(file_name):
    """Read the file and return both an iterator and the list of all lines."""
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return iter(lines), lines

def insert_word(word):
    """Insert the clicked word into the Entry widget."""
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, word)
    if altbuttonFlag.get():
        on_enter()

def on_enter(event=None):
    """Handle the Enter key event, updating the displayed text and saving if required."""
    if saveFlag.get():
        save_word(textbox.get())
    saveFlag.set(False)
    
    if textbox.get() != '':
        entered_text.set(f"{entered_text.get()}_{textbox.get()}")
    
    update_buttons()
    textbox.delete(0, tk.END)

def create_word_buttons(words):
    """Create buttons dynamically for each word in the list."""
    for word in words:
        button = tk.Button(bFrame, text=word, command=lambda w=word: insert_word(w))
        button.pack(side=tk.LEFT, pady=5, padx=5)
        buttons.append(button)

def clear_buttons():
    """Clear all buttons from the frame."""
    for btn in buttons:
        btn.destroy()
    buttons.clear()

def initialize_gui():
    """Set up the GUI components and configure the main window."""
    root.title("Line Reader")

    clm1 = tk.Label(root, textvariable=colstr1, font=('Arial', 12))
    clm1.pack(side=tk.TOP)

    bFrame.pack(side=tk.TOP)

    rb = tk.Checkbutton(inputFrame, text="Save Word?", variable=saveFlag)
    rb.pack(side=tk.LEFT)

    textbox.pack(side=tk.LEFT)
    inputFrame.pack(side=tk.TOP)

    result_label.pack(side=tk.TOP)

    # Fbuttonile menu
    buttonmenu = tk.Menu(menuBar, tearoff=0)
    buttonmenu.add_checkbutton(label="Alt Button",variable=altbuttonFlag)
    menuBar.add_cascade(label="Button", menu=buttonmenu)
    root.config(menu=menuBar)

    root.bind('<Return>', on_enter)

def get_time_PC():
    """Return the current PC time formatted as a string."""
    return datetime.now().strftime('%d-%b-%Y-%H:%M:%S')

def save_word(word):
    """Save the selected word to the current row in the file."""
    lines[current_row_index] = lines[current_row_index].strip(',\n') + f',{word}\n'
    
    with open(file_name, 'w') as file:
        file.writelines(lines)

def run_file_reader():
    """Main function to run the file reader and initialize the GUI."""
    global root, colstr1, entered_text, saveFlag, buttons, textbox, result_label, bFrame, inputFrame, menuBar
    global current_line, lines, current_row_index, file_name, altbuttonFlag

    root = tk.Tk()

    colstr1 = tk.StringVar()
    entered_text = tk.StringVar(value=get_time_PC())
    saveFlag = tk.BooleanVar(value=False)
    altbuttonFlag = tk.BooleanVar(value=True)
    buttons = []
    textbox = tk.Entry(inputFrame := tk.Frame(root), font=('Arial', 14), justify='center')
    result_label = tk.Label(root, textvariable=entered_text, font=('Arial', 12))
    bFrame = tk.Frame(root)
    menuBar = tk.Menu(root)

    file_name = "data_collection_template.csv"
    current_line, lines = read_file(file_name)
    current_row_index = 0

    try:
        first_words = next(current_line).strip(',\n').split(',')
        colstr1.set(first_words[0])
        create_word_buttons(first_words[1:])
    except StopIteration:
        colstr1.set("No more lines to read.")

    initialize_gui()
    
    root.mainloop()

    return entered_text.get()

if __name__ == '__main__':
    result = run_file_reader()
    print(result)
