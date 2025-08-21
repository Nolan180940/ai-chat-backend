# api/chat.py
from flask import Flask, request, jsonify
from openai import OpenAI
import os

# 创建 Flask 应用
app = Flask(__name__)

# 初始化 OpenAI 客户端（使用通义千问）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 从环境变量读取
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 通义千问兼容 OpenAI 的地址
)

@app.route('/', methods=['POST'])
def handle_chat():
    try:
        # 解析请求数据
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'reply': '请求错误：缺少 message 字段'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'reply': '请输入有效的问题'}), 400

        # 调用通义千问 API
        response = client.chat.completions.create(
            model="qwen-turbo",  # 推荐新手用 qwen-turbo（便宜、快）
            messages=[
                {"role": "system", "content": "你是一个友好、聪明的AI助手，名叫小智。回答要简洁、有帮助。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        # 提取 AI 回复
        ai_reply = response.choices[0].message.content
        return jsonify({'reply': ai_reply})

    except Exception as e:
        # 打印错误日志（在 Vercel Logs 中可见）
        print("❌ API Error:", str(e))
        return jsonify({
            'reply': '抱歉，AI 服务暂时不可用，请稍后再试。'
        }), 500

# Vercel Serverless 要求导出 handler
# 不要写 app.run()
handler = app