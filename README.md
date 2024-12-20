# Dynamic-TestFileName
A really badly made program that lets you modually construct a filename. Primarily meant to be used when collected data in segments.

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
     ```
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
     ```
     - In the above example, clicking `2.4` opens a folder allowing the user to choose a specific frequency (e.g., 2412 or 2437).  
     - If a row contains no further sub-options (like 5.7), the button acts normally without opening a folder.

### CSV Format:
- Each column represents a section of the final title.
- The first row in each column is the section's title.
- The remaining rows in that column contain the words users can select for that section.
- If a column lacks a title (empty first row), its words are grouped as sub-options to the left-most titled section.

Example excel:
```
Tests   Modulation  BW   Freq     -      -      -      Version
PSD     802.11a     20   2.4      2412   2437   2462   1
PWR     802.11n     40   5.1      5180   -      -      FINAL
OBW     -           80   5.7      -      -      -      -
```

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
