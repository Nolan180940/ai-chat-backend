# api/chat.py - 适配 openai==0.28.1
import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# 设置 API Key 和 Base URL
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"

@app.route('/', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'reply': '请求错误'}), 400

        user_message = data['message']

        response = openai.ChatCompletion.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": "你是一个友好、聪明的AI助手。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        ai_reply = response.choices[0].message.content
        return jsonify({'reply': ai_reply})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'reply': 'AI 服务出错，请稍后重试。'}), 500

# Vercel Serverless
handler = app