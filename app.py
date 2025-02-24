import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

app = Flask(__name__)

# 設定 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    essay = data.get("essay")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    try:
        # 使用 OpenAI 進行文本分析
        response = openai.Completion.create(
            model="text-davinci-003",  # 你可以根據需要使用不同的模型
            prompt=essay,
            max_tokens=150
        )

        result = response.choices[0].text.strip()
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
