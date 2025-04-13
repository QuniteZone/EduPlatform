import os
from openai import OpenAI
from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# 加载环境变量
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求


# 如果需要代理，取消以下注释并确保代理有效
# os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
# os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 获取用户输入
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # 初始化 OpenAI 客户端
        API_KEY = 'sk-QBFgXmIcXeaR5v40BZN3jabFKtSkoudkpIz4vmGU6V8Uu4N6'  # 替换为有效密钥
        BASE_URL = 'https://api.chatanywhere.tech/v1'  # 确保路径包含 /v1
        model_name = 'gpt-3.5-turbo'
        my_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        # 流式生成器函数
        def generate():
            try:
                response = my_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": user_message}],
                    stream=True
                )
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        yield (content + "\n").encode('utf-8')  # 转换为字节
            except Exception as e:
                error_msg = f"Error: {str(e)}\n".encode('utf-8')
                yield error_msg

        # 返回流式响应
        return Response(
            generate(),
            content_type='text/event-stream; charset=utf-8'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)