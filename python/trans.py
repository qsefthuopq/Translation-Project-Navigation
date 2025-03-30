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

    api_key = "输入DeepSeek的API"

    Language = "zh"

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        # Make the request to DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位精通游戏行业的翻译专家，你的任务是将文本准确地翻译成简体中文。请直接输出翻译，不要进行多余的分析；确保保留原文的语调、游戏术语和文化细微差别。请注意不要翻译原文的代码，比如\r和\n。翻译要求：多样性（Perplexity）衡量文本的复杂程度，反映了词汇的丰富性和不可预测性。更高的多样性表示内容更加多变并且更难预测。节奏感（Burstiness）则指句子长度和句式的波动幅度。高多样性和高节奏感的写作风格通常包含丰富的词汇、长短交替的句子，以及多样化的句式，这能让内容更生动和阅富有层次感。你的输出应必须展现高多样性和高节奏感。"},
                {"role": "user", "content": f"Translate the content to {Language} Language:\n\n<Start>{content}<End>"},
            ],
            stream=False
        )

        # Extract translated text
        trans = response.choices[0].message.content

        # Remove unnecessary tags
        trans = re.sub(r"<开始>|<结束>", "", trans)
        trans = re.sub(r"<start>|<end>", "", trans)
        trans = re.sub(r"<Start>|<End>", "", trans)

        # Return translated text
        return trans

    except Exception as e:
        # Handle potential errors during translation
        return f"An error occurred during translation: {e}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)