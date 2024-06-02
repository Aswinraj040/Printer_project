from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def print_file(filepath):
    if filepath.endswith(".pdf"):
        print_pdf(filepath)
    elif filepath.endswith(".docx"):
        print_docx(filepath)
    elif filepath.endswith(".png"):
        print_image(filepath)
    elif filepath.endswith(".jpg"):
        print_image(filepath)
    else:
        print("Unsupported file type")

def print_pdf(filepath):
    # Ensure file exists
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist")
        return

    subprocess.run(["lp", filepath], check=True)

def print_docx(filepath):
    # Ensure file exists
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist")
        return

    # Convert DOCX to PDF first
    from docx2pdf import convert
    pdf_path = filepath.replace(".docx", ".pdf")
    convert(filepath, pdf_path)
    print_pdf(pdf_path)

def print_image(filepath):
    # Ensure file exists
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist")
        return

    subprocess.run(["lp", filepath], check=True)

@app.route('/control_commands', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        try:
            print_file(filepath)
            return jsonify({'message': 'File uploaded and sent to printer successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Unknown error occurred'}), 500

@app.route('/testing_command', methods=['GET'])
def testing_command():
    return "Success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
