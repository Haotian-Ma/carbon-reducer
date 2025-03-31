from flask import Flask, jsonify, request

app = Flask(__name__)

# 测试接口，返回一个简单的 JSON
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello from Flask backend!"})

# 如果需要其他接口，就继续写

if __name__ == '__main__':
    # 开发环境下用下面这行测试运行。生产环境推荐用 Gunicorn + Nginx
    app.run(host='0.0.0.0', port=5000, debug=True)
