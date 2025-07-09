from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Compiler import ASMParser, ASMFile
from werkzeug.utils import secure_filename
import tempfile


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": os.getenv('CLIENT_ORIGIN')}},supports_credentials=True)

# Configuration for file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'asm', 'jack', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/asmtohack", methods=['POST'])
def asm_to_hack():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', 'assembly')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if language == 'assembly' or filename.endswith('.asm'):
            asm_processor = ASMFile(filepath)
            hack_instructions = "\n".join(asm_processor.hackInstructions)
            
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'hack_code': hack_instructions,
                'message': 'Assembly file converted successfully',
                'filename': filename
            })
        else:
            os.remove(filepath)
            return jsonify({'error': 'Unsupported file type'}), 400
            
    except Exception as e:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing file'
        }), 500
    
@app.route("/test", methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Test endpoint is working'}), 200

if __name__ == "__main__":
       app.run(
           host="0.0.0.0",
           port=os.getenv("FLASK_PORT"),
           debug=True,
           use_reloader=True
       )