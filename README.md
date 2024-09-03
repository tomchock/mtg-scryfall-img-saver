## Description

This is a Python tool designed to download Magic: The Gathering card images and the complete set list in CSV format from Scryfall. 
The tool provides a graphical user interface to input the URL of a Scryfall page and select a destination folder for saving them. 
The CSV file will include the following information: set name, card number, card name, card color, rarity.
Card images are saved with a progressive numbering system that matches the card number in the CSV.

## How to Use

1. **Run the Script**: Open the .bat file or execute the Python script directly. This will open a graphical interface.

2. **Enter URL**: When prompted, enter the URL of the page. (ex. https://scryfall.com/sets/drk )

3. **Select Directory**: Choose the folder where you want to save the downloaded images and CSV.

4. **Download**: The tool will start downloading the files and save them in the selected directory with cleaned filenames.


## Requirements

- Python 3.x
- The following Python libraries:
  - requests
  - beautifulsoup4
  - tkinter

  
---

Feel free to modify it based on your specific project details or preferences!
