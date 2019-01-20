# form-grader
	
This is a package for reading and auto-grading multiple answer forms.

### Features
#### Creating tests using [Google Script API](https://developers.google.com/apps-script/reference/)

### TODO
- [ ] Add export to csv
- [ ] Add Excel support
- [ ] Add parameter to specify number of answers (possibly another excel file)
- [ ] Create NN that recognizes rows of squares and squares themselves in image
- [ ] Handle case when no circle is scratched &rarr; add minimum amount of black pixels depending on the image resolution

### Dependencies
#### Tesseract
This project is using [Tesseract](https://github.com/tesseract-ocr/tesseract) OCR engine developed by Google. To install it on Linux use 

    sudo apt install tesseract-ocr
    sudo apt install libtesseract-dev

For other systems, the install instructions can be found [here](https://github.com/tesseract-ocr/tesseract/wiki)

Language used here is Croatian, but all other language models can be found [here](https://github.com/tesseract-ocr/tessdata). In order to use other lanuages, the unpacked `.traineddata` file has to be moved to `tessdata` directory. The directory can be found in several locations (depending on the type of the training data and the Linux ditribution). Possibilities are `/usr/share/tesseract-ocr/tessdata` or `/usr/share/tessdata` or `/usr/share/tesseract-ocr/4.00/tessdata`