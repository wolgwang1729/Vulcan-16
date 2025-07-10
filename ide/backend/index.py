from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Compiler import *
from werkzeug.utils import secure_filename
import tempfile
import shutil

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": os.getenv('CLIENT_ORIGIN')}}, supports_credentials=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'asm', 'jack', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/asmtohack", methods=['POST'])
def asm_to_hack():
    temp_dir = None
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', 'assembly')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        temp_dir = tempfile.mkdtemp(prefix='asm_upload_')
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        if language == 'assembly' or filename.endswith('.asm'):
            asm_processor = ASMFile(filepath)
            hack_instructions = "\n".join(asm_processor.hackInstructions)
            return jsonify({
                'success': True,
                'hack_code': hack_instructions,
                'message': 'Assembly file converted successfully',
                'filename': filename
            })
        elif language == 'vm' or filename.endswith('.vm'):
            vm_processor = VMTranslatorFile(filepath)
            assembly_instructions = "\n".join(vm_processor.assemblyInstructions)
            return jsonify({
                'success': True,
                'hack_code': assembly_instructions,
                'message': 'VM file converted successfully',
                'filename': filename
            })

        else:
            return jsonify({'error': 'Unsupported file type'}), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing file'
        }), 500
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

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
