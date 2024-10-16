# Simple script collection for OCR
Currently uses tesseract.

## Installation
First install Tesseract
```
sudo apt update
sudo apt install tesseract
```
Then create a venv using python 3.11.2
```
python3 -m venv -r requirements.txt
```
## Usage
Populate the "images" folder with images you want to process.
```
chmod +x main.py
./main.py
```
 The script will look for written serial numbers (starting with S/N) and add them to 'output.txt' in a json format. Currently, the script does 2 passes with 2 different algorithms, so the data can be present twice.
