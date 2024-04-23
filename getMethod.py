from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求

# 模拟的数据源
data_source = {
    'users': ['Alice', 'Bob', 'Charlie', 'David'],
    'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

# 处理跨域 GET 请求的路由
def get_data():
    try:
        # 模拟数据源的 URL
        data_url = 'http://localhost:5000/mock/data'  # 这里假设数据源服务在本地运行

        # 发起 GET 请求到模拟数据源
        response = requests.get(data_url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 返回获取的数据，这里假设数据是 JSON 格式
            return jsonify(response.json())

        # 如果请求不成功，返回错误信息
        return jsonify({'error': 'Failed to fetch data from the data source'}), 500

    except Exception as e:
        # 处理异常情况
        return jsonify({'error': str(e)}), 500

# 模拟数据源的路由
@app.route('/mock/data', methods=['GET'])
def mock_data():
    # 模拟数据源返回数据
    return jsonify(data_source)

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
