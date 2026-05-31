// Elements
const fileInput = document.getElementById('file-input');
const dropContainer = document.querySelector('.drop-container');
const detectedText = document.getElementById('detected-text');
const detectedLanguage = document.getElementById('detected-language');
const translateBtn = document.getElementById('translate-btn');
const languageSelect = document.getElementById('language-select');
const translatedText = document.getElementById('translated-text');
const errorMessage = document.getElementById('error-message');

// Image Preview and Controls
const imagePreview = document.getElementById('image-preview');
const imagePreviewContainer = document.querySelector('.image-preview-container');
const imageName = document.getElementById('image-name');
const imageControls = document.querySelector('.image-controls');

// Handwriting toggle
const handwritingToggle = document.getElementById('handwriting-toggle');

// Variables for transformations
let zoomLevel = 1; // Initial zoom level
let rotationAngle = 0; // Initial rotation angle

// Highlight drop area on dragover
dropContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropContainer.style.backgroundColor = 'rgba(0, 140, 255, 0.2)';
    dropContainer.style.borderColor = 'rgba(17, 17, 17, 0.8)';
});

// Reset drop area style on dragleave
dropContainer.addEventListener('dragleave', () => {
    dropContainer.style.backgroundColor = '';
    dropContainer.style.borderColor = 'rgb(171, 202, 255)';
});

// Handle drop event
dropContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    dropContainer.style.backgroundColor = '';
    dropContainer.style.borderColor = 'rgb(171, 202, 255)';

    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files; // Update file input with the dropped file
        handleFileUpload(file); // Process the dropped file
    }
});

// Handle file selection via the file input
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file); // Process the selected file
    } else {
        errorMessage.textContent = 'No file selected. Please choose a valid file.';
    }
});

// Function to upload and process the file
function handleFileUpload(file) {
    errorMessage.textContent = ''; // Clear previous errors
    detectedText.textContent = 'Processing...'; // Indicate processing
    detectedLanguage.textContent = ''; // Clear previous language detection
    translatedText.textContent = ''; // Clear previous translation

    // Display the image preview
    const imageUrl = URL.createObjectURL(file);
    imagePreview.src = imageUrl;
    imageName.textContent = file.name;

    // Show image preview and tools
    imagePreviewContainer.querySelector('.hidden').classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('handwriting_mode', handwritingToggle.checked);  // Add handwriting mode flag

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                errorMessage.textContent = data.error;
                detectedText.textContent = 'No text detected.';
            } else {
                detectedText.textContent = data.text || 'No text detected.';
                detectedLanguage.textContent = `Language: ${data.language || 'Unknown'}`;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred while processing the file.';
            detectedText.textContent = 'No text detected.';
        });
}


// Reset Image functionality
document.getElementById('reset-image').addEventListener('click', () => {
    zoomLevel = 1;
    rotationAngle = 0;
    applyTransformations();
});

// Function to copy text to clipboard
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    alert("Text copied to clipboard!");
}

// Add event listeners for the copy buttons
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        if (event.target.classList.contains('copyBtn')) {
            const targetTextId = event.target.getAttribute('data-target');
            const textContent = document.getElementById(targetTextId).textContent;
            copyToClipboard(textContent);
        }
    });
});

// Handle translate button click
translateBtn.addEventListener('click', () => {
    const text = detectedText.textContent;
    const targetLang = languageSelect.value;

    translatedText.textContent = 'Processing...';  // Show "Processing..." during translation
    errorMessage.textContent = ''; // Clear previous error messages

    if (!text || text === 'Processing...' || text === 'No text detected.') {
        errorMessage.textContent = 'No text available for translation.';
        return;
    }

    const requestData = {
        text: text,
        target_lang: targetLang,
    };

    fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                errorMessage.textContent = data.error;
                translatedText.textContent = 'No translation available.';
            } else {
                translatedText.textContent = data.translated_text || 'No translation available.';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred during translation.';
            translatedText.textContent = 'No translation available.';
        });
});
