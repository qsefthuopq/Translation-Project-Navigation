from flask import Flask, request
import requests
import re

app = Flask(__name__)

OLLAMA_API_URL = "http://39.170.70.250:11434/api/chat"

def protect_special_chars(text):
    """保护特殊字符不被翻译，使用Unicode私有区域字符替代"""
    # 使用Unicode私有区域字符替代特殊字符
    return text.replace('\n', '\ue000').replace('\r', '\ue001')

def restore_special_chars(text):
    """恢复被保护的Unicode私有区域字符为原始特殊字符"""
    return text.replace('\ue000', '\n').replace('\ue001', '\r')

@app.route('/translate', methods=['get'])
def translate():
    content = request.args.get('text')

    if content is None:
        return "Missing text content in request!"

    Language = "zh"

    try:
        # 预处理保护特殊字符
        protected_content = protect_special_chars(content)
        
        data = {
            "model": "nezahatkorkmaz/deepseek-v3:latest",
            "messages": [
                {"role": "system", "content": "你是一位精通游戏行业的翻译专家，你的任务是将文本准确地翻译成简体中文。请直接输出翻译，不要进行多余的分析；确保保留原文的语调、游戏术语和文化细微差别。请注意不要翻译原文的代码，比如\r和\n。翻译要求：多样性（Perplexity）衡量文本的复杂程度，反映了词汇的丰富性和不可预测性。更高的多样性表示内容更加多变并且更难预测。节奏感（Burstiness）则指句子长度和句式的波动幅度。高多样性和高节奏感的写作风格通常包含丰富的词汇、长短交替的句子，以及多样化的句式，这能让内容更生动和阅富有层次感。你的输出应必须展现高多样性和高节奏感。"},
                {
                    "role": "user",
                    "content": f"将以下内容翻译成{Language}语言（请严格保留所有[NEWLINE]和[RETURN]标记）：\n{processed_content}"
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.3  # 降低随机性，提高确定性
        }

        response = requests.post(
            OLLAMA_API_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code != 200:
            return f"API request failed with status code {response.status_code}: {response.text}"

        response_data = response.json()
        trans = response_data["message"]["content"]

        # 恢复特殊字符
        trans = restore_special_chars(trans)
        
        # 彻底清除任何可能残留的标记
        trans = re.sub(r'<\/?(?:[Ee]nd|[Ss]tart|开始|结束)>?', '', trans)
        trans = re.sub(r'<[^>]+>', '', trans)
        trans = trans.strip()

        return trans

    except Exception as e:
        return f"An error occurred during translation: {str(e)}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)