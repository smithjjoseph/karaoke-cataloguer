# Karaoke Cataloguer
Applications for cataloguing karaoke CDs

## main.py
A GUI entry point for selecting between input and output applications

![Main Sample Image Missing!](./assets/main.png "Main Sample Image")

Note: It is a known issue that using multiple CTk instances creates some rubbish output in the terminal - this does not affect usage of the GUI

## input.py
A GUI for inputting CD titles and tracks into the karaoke database

- CD images can be browsed through using "Previous Image" and "Next Image" buttons
- Title and Tracks can be inputted using OCR assistance
  - Drag to select area to use OCR and enter to finish selection
  - If a mistake is made a new selection can be made or 'q' used to exit the cropping tool
- Corrections to OCR input can be made using text boxes on the right
  - The image can be selected if a quick preview is needed
- When all required changes/additions have been made the "Submit to DB" can be selected and the application closed

<br>

![Input Sample Image Missing!](./assets/input.png "Input Sample Image")

## output.py
A GUI for easily finding CD titles and tracks in the karaoke database

- Tracks can be searched through the entry at the top of the window
- Results will be displayed in the table below

![Output Sample Image Missing!](./assets/output.png "Output Sample Image")

## ocr.py
Helper class for OCR related functionality