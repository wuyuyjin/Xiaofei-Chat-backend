from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求


# 定义一个接受 POST 请求的路由
@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        # 从 POST 请求中获取 JSON 数据
        data = request.get_json()

        if data:
            # 假设请求包含一个名为 'name' 的字段
            name = data.get('name')

            if name:
                response = {'message': f'Hello, {name}! Your request was successful.'}
                return jsonify(response), 200
            else:
                return jsonify({'error': 'Name not provided in request.'}), 400
        else:
            return jsonify({'error': 'Invalid JSON in request.'}), 400
    else:
        return jsonify({'error': 'Only POST requests are allowed.'}), 405


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
