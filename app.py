import os
import openai
from flask import Flask, request, jsonify

# 設置 OpenAI API 密鑰
openai.api_key = os.getenv("OPENAI_API_KEY")  # 或將這行替換為 openai.api_key = 'your-api-key'，但不建議寫死密鑰

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to AI Essay Review! Your service is up and running.'

@app.route('/evaluate', methods=['POST'])
def evaluate_essay():
    try:
        # 獲取文章內容
        data = request.get_json()
        essay = data.get('essay')

        if not essay:
            return jsonify({"error": "No essay provided"}), 400

        # 發送請求到 OpenAI API 進行評估
        response = openai.Completion.create(
            engine="text-davinci-003",  # 或者使用你需要的引擎，這裡以 text-davinci-003 為例
            prompt=essay,
            max_tokens=500,
            temperature=0.7,
        )

        feedback = response.choices[0].text.strip()  # 提取 API 回應中的文本

        return jsonify({"feedback": feedback})

    except Exception as e:
        # 如果有錯誤，捕捉並返回錯誤訊息
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)  # 設定端口為 10000，並啟用 debug 模式
