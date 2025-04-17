from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import docx  # python-docx

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(path):
    text = ''
    pdf = fitz.open(stream=path.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(path):
    text = ''
    doc = docx.Document(path)
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

@app.route('/plan/lesson_script', methods=['POST'])
def handle_lesson_script():
    transcription_requirements = request.form.get('require', '')
    uploaded_files = request.files.getlist('files')
    parsed_texts = {}
    content = {}  # 返回结构

    if not uploaded_files:
        content["status"] = -1  # 表示文件未上传
        content["content"] = None

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()  # 直接读取文件内容
            if ext == 'pdf':
                parsed_text = extract_text_from_pdf(file.stream)  # 使用 file.stream 直接读取
            else:
                parsed_text = extract_text_from_docx(file.stream)  # 使用 file.stream 直接读取
            parsed_texts[file.filename] = parsed_text
        else:
            content["status"] = -2  # 不支持该文件类型
            content["content"] = None


    content["content"] = f"这是逐字稿, 逐字稿要求: {transcription_requirements} + '解析' + {parsed_texts}"
    content["status"] = 1
    print(f"content: {content}")
    return jsonify(content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)