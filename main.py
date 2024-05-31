import base64
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from tushengwen import tushengwen
from wenshengtu import wenshengtu
from upload_to_qiniu import upload_to_qiniu

app = Flask(__name__)
CORS(app)  # 允许跨域请求

dataResult = ""


# 定义一个接受 POST 请求的路由
@app.route('/wenshengtu', methods=['POST'])
def wenshengtu_data():
    if request.method == 'POST':
        # 从 POST 请求中获取 JSON 数据
        data = request.get_json()

        if data:
            # 假设请求包含一个名为 'name' 的字段
            content = data.get('content')
            wenshengtu(content)
            if content:
                response = {'message': f'Hello, {content}! Your request was successful.'}

                return jsonify(response), 200
            else:
                return jsonify({'error': 'content not provided in request.'}), 400
        else:
            return jsonify({'error': 'Invalid JSON in request.'}), 400
    else:
        return jsonify({'error': 'Only POST requests are allowed.'}), 405


@app.route('/tushengwen', methods=['POST'])
def tushengwen_data():
    if request.method == 'POST':
        # 检查是否上传了文件和其他数据
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        content = request.form.get('chat')

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 处理文件和其他数据
        filename = secure_filename(file.filename)  # 需要导入 secure_filename 函数
        app.config['UPLOAD_FOLDER'] = 'public'  # 设置上传文件的目标文件夹路径
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        filePath = f"public/{filename}"
        upload_to_qiniu(filePath)
        # upload_to_qiniu()
        print("file:",file)
        tushengwen(content,filename,my_callback)

        if dataResult:
            # 响应消息
            response = {
                'message': f'{dataResult}',
            }
            return jsonify(response), 200

def my_callback(result):
    global dataResult
    dataResult = result
    print("收到的结果：", result)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
