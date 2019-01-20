# form-grader
	
This is a package for reading and auto-grading multiple answer forms.

### Features
#### 1. Creating tests
Creating tests using [Google Script API](https://developers.google.com/apps-script/reference/) &rarr; decide what to use: Docs or Forms

### TODO
Trello: 
 - [Prototype board](https://trello.com/b/EQwEYpGS/prototype) 
 - [Full board](https://trello.com/b/Yib9xFoY/develop)

### Dependencies
#### Tesseract
This project is using [Tesseract](https://github.com/tesseract-ocr/tesseract) OCR engine developed by Google. To install it on Linux use 

    sudo apt install tesseract-ocr
    sudo apt install libtesseract-dev

For other systems, the install instructions can be found [here](https://github.com/tesseract-ocr/tesseract/wiki)

Language used here is Croatian, but all other language models can be found [here](https://github.com/tesseract-ocr/tessdata). In order to use other lanuages, the unpacked `.traineddata` file has to be moved to `tessdata` directory. The directory can be found in several locations (depending on the type of the training data and the Linux ditribution). Possibilities are `/usr/share/tesseract-ocr/tessdata` or `/usr/share/tessdata` or `/usr/share/tesseract-ocr/4.00/tessdata`