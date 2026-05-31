from flask import Flask, render_template, request, jsonify
import easyocr
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from googletrans import Translator
import pytesseract

import sqlite3  # SQLite3 is built into Python

def init_db():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    conn = sqlite3.connect('ocr_data.db')  # Connect to the SQLite database (creates the file if not exists)
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands

    # SQL command to create the `ocr_records` table (this was missing in your code)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocr_records (  -- Change to 'ocr_records'
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier
            image_name TEXT NOT NULL,              -- Image file name
            image_data BLOB NOT NULL,              -- Image binary data
            extracted_text TEXT NOT NULL,          -- Extracted text from the image
            detected_language TEXT NOT NULL,       -- Detected language of the extracted text
            translated_text TEXT,                  -- Translated text (optional)
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Automatically store the timestamp
        )
    ''')
    conn.commit()  # Commit the changes
    conn.close()   # Close the connection



# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

import pyocr
import pyocr.builders
import cv2
import os


from PIL import Image

app = Flask(__name__)

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Define language groups based on compatibility
language_groups = [
    ['af', 'en'],  # Afrikaans with English
    ['ar', 'en'],  # Arabic with English
    ['az', 'en'],  # Azerbaijani with English
    ['bg', 'en'],  # Bulgarian with English
    ['bn', 'en'],  # Bengali with English
    ['ch_sim', 'en'],  # Simplified Chinese with English
    ['ch_tra', 'en'],  # Traditional Chinese with English
    ['cs', 'en'],  # Czech with English
    ['da', 'en'],  # Danish with English
    ['de', 'en'],  # German with English
    ['en'],  # English alone
    ['es', 'en'],  # Spanish with English
    ['et', 'en'],  # Estonian with English
    ['fa', 'en'],  # Persian (Farsi) with English
    ['fr', 'en'],  # French with English
    ['ga', 'en'],  # Irish with English
    ['hi', 'en'],  # Hindi with English
    ['hr', 'en'],  # Croatian with English
    ['hu', 'en'],  # Hungarian with English
    ['id', 'en'],  # Indonesian with English
    ['it', 'en'],  # Italian with English
    ['ja', 'en'],  # Japanese with English
    ['kn', 'en'],  # Kannada with English
    ['ko', 'en'],  # Korean with English
    ['ku', 'en'],  # Kurdish with English
    ['la', 'en'],  # Latin with English
    ['lv', 'en'],  # Latvian with English
    ['mr', 'en'],  # Marathi with English
    ['ms', 'en'],  # Malay with English
    ['mt', 'en'],  # Maltese with English
    ['ne', 'en'],  # Nepali with English
    ['nl', 'en'],  # Dutch with English
    ['no', 'en'],  # Norwegian with English
    ['pl', 'en'],  # Polish with English
    ['pt', 'en'],  # Portuguese with English
    ['ro', 'en'],  # Romanian with English
    ['ru', 'en'],  # Russian with English
    ['sk', 'en'],  # Slovak with English
    ['sl', 'en'],  # Slovenian with English
    ['sq', 'en'],  # Albanian with English
    ['sv', 'en'],  # Swedish with English
    ['ta', 'en'],  # Tamil with English
    ['te', 'en'],  # Telugu with English
    ['th', 'en'],  # Thai with English
    ['tl', 'en'],  # Filipino (Tagalog) with English
    ['tr', 'en'],  # Turkish with English
    ['uk', 'en'],  # Ukrainian with English
    ['ur', 'en'],  # Urdu with English
    ['vi', 'en'],  # Vietnamese with English
]

# Choose appropriate language group based on input or use a default
selected_languages = ['en', 'hi']  # Example for Hindi and English
reader = easyocr.Reader(selected_languages, gpu=False)


# Initialize Google Translate
translator = Translator()

def preprocess_image(file_path):
    """Preprocess the uploaded image for OCR."""
    image = cv2.imread(file_path)   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def pytesseract_ocr(image_path):
    """Use pytesseract for OCR."""
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error with pytesseract: {e}"

def pyocr_tool(image_path):
    """Use pyocr for OCR."""
    try:
        tools = pyocr.get_available_tools()
        if not tools:
            return "No OCR tool found in pyocr."
        tool = tools[0]
        image = Image.open(image_path)
        return tool.image_to_string(image, builder=pyocr.builders.TextBuilder())
    except Exception as e:
        return f"Error with pyocr: {e}"
    
def handwriting_ocr(file_path):
    """
    Perform handwriting recognition using OCR tools.
    """
    try:
        # Load the image
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Apply preprocessing steps (enhancing text visibility)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR using Tesseract (PSM mode for handwriting)
        text = pytesseract.image_to_string(thresh, config='--psm 7')  # PSM 7 is good for a single line
        return text.strip()

    except Exception as e:
        return f"Error with handwriting OCR: {e}"
    
def get_ocr_records():
    """Fetch all OCR records from the database."""
    conn = sqlite3.connect('ocr_data.db')
    cursor = conn.cursor()

    # Query to fetch all records from ocr_records table, including all necessary columns
    cursor.execute("SELECT id, image_name, image_data, extracted_text, detected_language, translated_text, timestamp FROM ocr_records")
    records = cursor.fetchall()  # Fetch all rows as a list of tuples
    conn.close()

    return records



@app.route('/')
def landing_page():
    """Render the landing page."""
    return render_template('landing.html')

@app.route('/tool')
def index():
    """Render the main OCR and translation tool."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload and perform OCR with an option for handwriting recognition.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'})

    handwriting_mode = request.form.get('handwriting_mode', 'false').lower() == 'true'
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(file_path)

    try:
        
        # Convert the uploaded image to binary
        with open(file_path, 'rb') as img_file:
            image_binary = img_file.read()
            
        # Preprocess the image
        image = preprocess_image(file_path)

        # Perform handwriting OCR if handwriting mode is enabled
        if handwriting_mode:
            extracted_text = handwriting_ocr(file_path)
        else:
            # Perform OCR using EasyOCR
            result = reader.readtext(image)
            extracted_text = ' '.join([res[1] for res in result if res[2] > 0.5])

            # Fallback to Tesseract or PyOCR if EasyOCR doesn't find text
            if not extracted_text.strip():
                extracted_text = pytesseract_ocr(file_path) or pyocr_tool(file_path)

        if not extracted_text.strip():
            return jsonify({'error': 'No text detected in the image.'})

        try:
            detected_language = detect(extracted_text)
        except LangDetectException:
            detected_language = 'unknown'
        
        # Insert data into the database
        conn = sqlite3.connect('ocr_data.db')
        cursor = conn.cursor()
        cursor.execute(
             '''
    INSERT INTO ocr_records (image_name, image_data, extracted_text, detected_language,  translated_text)
    VALUES (?, ?, ?, ?, ?)
    ''',
    (file.filename, image_binary, extracted_text, detected_language, None)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'text': extracted_text,
            'language': detected_language
        })

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        os.remove(file_path)  # Clean up temporary file

        
 

@app.route('/translate', methods=['POST'])
def translate_text():
    """Translate extracted text to a target language using GoogleTrans."""
    data = request.json
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')  # Default to English

    if not text.strip():
        return jsonify({'error': 'No text to translate.'})

    try:
        # Translate the text
        translation = translator.translate(text, dest=target_lang)

        # Store the translation in the database
        conn = sqlite3.connect('ocr_data.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE ocr_records
            SET translated_text = ?
            WHERE extracted_text = ?
            ''',
            (translation.text, text)
        )
        conn.commit()
        conn.close()

        return jsonify({'translated_text': translation.text})

    except Exception as e:
        return jsonify({'error': str(e)})

import base64  # Import for encoding images

@app.route('/records')
def show_records():
    """Fetch and display all OCR records with images."""
    conn = sqlite3.connect('ocr_data.db')
    cursor = conn.cursor()

    # Fetch all records including image_data
    cursor.execute("SELECT id, image_name, image_data, extracted_text, detected_language, translated_text, timestamp FROM ocr_records")
    rows = cursor.fetchall()
    conn.close()

    # Process records to include Base64-encoded images
    records = []
    for row in rows:
        image_data = base64.b64encode(row[2]).decode('utf-8') if row[2] else None  # Encode binary data
        records.append({
            'id': row[0],
            'image_name': row[1],
            'image_data': image_data,  # Base64-encoded image
            'extracted_text': row[3],
            'detected_language': row[4],
            'translated_text': row[5],
            'timestamp': row[6]
        })
        
        records = sorted(records, key=lambda x: x['timestamp'], reverse=True)


    return render_template('records.html', records=records)



if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)  # Start the Flask application
