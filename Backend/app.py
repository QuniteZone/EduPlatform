from flask import Flask, jsonify


app = Flask(__name__)

# 导入蓝图
from Apps.lesson_plan import lesson_plan_bp
from Apps.ppt_generator import ppt_generator_bp

# 注册蓝图
app.register_blueprint(lesson_plan_bp, url_prefix='/lesson')  # 可以设置 URL 前缀
app.register_blueprint(ppt_generator_bp, url_prefix='/ppt')  # 可以设置 URL 前缀


@app.route('/')
def home():
    return "你好呀！！"  # 渲染名为 index.html 的模板

@app.route('/api/test', methods=['GET'])
def test():
    # 自定义字符串
    return jsonify({"message": "Hello from Flask backend!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)