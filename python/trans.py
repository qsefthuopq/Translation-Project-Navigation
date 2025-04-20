from flask import Flask, request
import requests
import json
import re
from openai import OpenAI

app = Flask(__name__)

@app.route('/translate', methods=['get'])
def translate():
    content = request.args.get('text')

    # Check if 'text' parameter is missing
    if content is None:
        return "Missing text content in request!"

    api_key = "输入deepseek的API"

    Language = "zh"

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        # Make the request to DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位精通多语种游戏本地化的专业译员，请严格遵循以下准则进行中文本地化：\n"
                 "1. 仅输出最终译文，禁止任何分析/注释/说明\n"
                 "2. 保留专业术语的英文缩写（如2E/DLC/MMO）\n"
                 "3. 动态调整句式结构，采用长短句交替的节奏\n"
                 "4. 保持原文隐含的叙事张力和玩家视角"},
                {"role": "user", "content": f"以专业游戏汉化风格翻译该内容：\n\n{content}"}
            ],
            stream=False
        )

        # Extract translated text
        trans = response.choices[0].message.content

        # Return translated text
        return trans

    except Exception as e:
        # Handle potential errors during translation
        return f"An error occurred during translation: {e}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
