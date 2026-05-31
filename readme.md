
# OCR and Multilingual Translator Web Application

## Overview
The OCR and Translator Web Application is a robust solution for extracting text from images, detecting its language, and translating it into multiple languages. This application is designed to enhance accessibility and cross-cultural communication by enabling seamless text recognition and translation. The project incorporates advanced OCR technologies like EasyOCR, PyTesseract, and handwriting recognition, combined with the Google Translate API for dynamic translations.

## Features
- **Image Upload and Drag-and-Drop Functionality**: Supports uploading images through file input and drag-and-drop.
- **Text Extraction**: Leverages EasyOCR and PyTesseract for extracting text from images.
- **Handwriting Recognition**: Includes a mode for recognizing handwritten text.
- **Language Detection**: Automatically identifies the language of the extracted text using `langdetect`.
- **Translation**: Translates text into a wide range of languages using Google Translate API.
- **Database Integration**: Stores OCR and translation results in an SQLite database for easy retrieval and analysis.
- **User-Friendly Interface**: Features a modern and responsive UI with features like text copying and image previews.

## Technology Stack
- **Frontend**:
  - HTML, CSS, JavaScript
  - Responsive design and gradient themes for a professional look
- **Backend**:
  - Python (Flask framework)
  - EasyOCR, PyTesseract, PyOCR for OCR functionalities
  - Google Translate API for translations
  - SQLite for data storage
- **APIs and Libraries**:
  - EasyOCR
  - Googletrans (Google Translate API)
  - Langdetect (Language detection)
  - PyTorch (Required for EasyOCR)

## Project Structure
OCR_Translator/
│
├── app.py                  # Flask application and backend logic
├── ocr_data.db             # SQLite database storing OCR and translation records
├── requirements.txt        # Python dependencies
│
├── templates/              # HTML templates for Flask
│   ├── index.html          # Main OCR and translation tool page
│   ├── landing.html        # Landing page with project overview
│   └── records.html        # Page displaying OCR records from the database
│
├── static/                 # Static files for CSS, JavaScript, and images
│   ├── styles.css          # Styles for index.html and records.html
│   ├── landing.css         # Styles for landing.html
│   ├── script.js           # JavaScript for index.html
│   ├── landing.js          # JavaScript for landing.html
│   └── images/             # Images used in the landing page
│       ├── text_extraction.png
│       ├── language_detection.png
│       ├── translation.png
│       └── user_friendly.png


## Installation and Setup
### Prerequisites
- Python 3.x installed
- Tesseract OCR installed (Ensure `tesseract.exe` is added to the system PATH)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/OCR_Translator.git
   cd OCR_Translator

2. Install dependencies:
bash
pip install -r requirements.txt

3. Initialize the database:
The database will be created automatically when the Flask application runs.
4. Run the application:
bash
python app.py

5. Open your browser and navigate to:

http://127.0.0.1:5000/

Usage
	1.	Landing Page: Navigate to the tool page from the landing page.
	2.	OCR and Translation:
	•	Upload an image or drag-and-drop it into the upload section.
	•	Enable “Handwriting Recognition” if processing handwritten text.
	•	View the extracted text, detected language, and translation.
	3.	View Records: Access OCR records, including images, via the /records route.

Features in Detail
	•	Text Extraction: Supports multilingual text detection with EasyOCR and PyTesseract fallback.
	•	Handwriting Mode: Preprocesses and extracts handwritten text using Tesseract’s handwriting mode.
	•	Dynamic Language Translation: Translate text into Indian languages (Hindi, Kannada, Tamil, etc.) and popular global languages (French, Spanish, German, etc.).
	•	Database Integration: Stores records for future reference, including timestamps and translations.

Future Enhancements
	•	Add real-time OCR and translation via live camera feed.
	•	Deploy the application to cloud platforms like AWS or Heroku.
	•	Extend handwriting recognition to support complex cursive styles.

Dependencies
	•	Python 3.x
	•	Flask
	•	EasyOCR
	•	PyTesseract
	•	PyTorch
	•	Googletrans
	•	Langdetect
	•	OpenCV
	•	SQLite3

Acknowledgements
	•	EasyOCR Documentation: https://www.jaided.ai/easyocr/
	•	Google Translate API: https://cloud.google.com/translate
	•	Tesseract OCR: https://github.com/tesseract-ocr/tesseract
