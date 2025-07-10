from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Compiler import *
from werkzeug.utils import secure_filename
import tempfile
import zipfile
import json
import shutil

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": os.getenv('CLIENT_ORIGIN')}}, supports_credentials=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'asm', 'jack', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/compile", methods=['POST'])
def compile():
    temp_dir = None
    try:
        language = request.form.get('language', 'assembly')
        is_folder = request.form.get('is_folder', 'false').lower() == 'true'
        target_language = request.form.get('target', '.hack')
        
        temp_dir = tempfile.mkdtemp(prefix='temp_compilation_')
        
        if is_folder and language == 'jack':
            # Handle folder compilation
            folder_name = request.form.get('folder_name')
            if not folder_name:
                return jsonify({'error': 'Folder name not provided'}), 400
            
            # Get all files
            files = request.files.getlist('files')
            if not files:
                return jsonify({'error': 'No files provided for folder compilation'}), 400
            
            # Create folder structure and save files
            folder_path = os.path.join(temp_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(folder_path, filename)
                    file.save(filepath)
            
            # Run JackCompiler on the folder
            try:
                jack_compiler = JackCompiler(folder_path)
                
                # Look for the generated .hack file
                hack_filename = f"{folder_name}.hack"
                hack_filepath = os.path.join(folder_path, hack_filename)
                
                if os.path.exists(hack_filepath):
                    with open(hack_filepath, 'r') as hack_file:
                        hack_content = hack_file.read()
                    
                    return jsonify({
                        'success': True,
                        'hack_code': hack_content,
                        'message': f'Folder {folder_name} compiled successfully',
                        'filename': hack_filename
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Compilation completed but {hack_filename} not found',
                        'message': 'Jack compilation may have failed'
                    }), 500
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'JackCompiler error: {str(e)}',
                    'message': 'Error during Jack compilation'
                }), 500
        
        else:
            # Handle single file compilation (existing logic)
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
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
                asm_filename = f"{filename.rsplit('.', 1)[0]}.asm"
                asm_filepath = os.path.join(temp_dir, asm_filename)
                
                if os.path.exists(asm_filepath):
                    with open(asm_filepath, 'r') as asm_file:
                        asm_instructions = asm_file.read()
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Compilation completed but {asm_filename} not found',
                        'message': 'VM translation may have failed'
                    }), 500
                
                if target_language == '.asm':
                    return jsonify({
                        'success': True,
                        'asm_code': asm_instructions,
                        'message': 'VM file converted successfully',
                        'filename': asm_filename
                    })
                
                elif target_language == '.hack':
                    asm_processor = ASMFile(asm_filepath)
                    hack_instructions = "\n".join(asm_processor.hackInstructions)
                    hack_filename = f"{filename.rsplit('.', 1)[0]}.hack"
                    return jsonify({
                        'success': True,
                        'hack_code': hack_instructions,
                        'message': 'VM file converted to Hack successfully',
                        'filename': hack_filename
                    })
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing compilation request'
        }), 500
    
    finally:
        # Clean up temp directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # Ignore cleanup errors

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
