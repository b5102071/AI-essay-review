import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

# 使用 Render 提供的環境變數
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    essay = data.get("essay")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    try:
        # 使用 OpenAI 進行文本分析，將 max_tokens 設為 10000
        response = openai.Completion.create(
            model="text-davinci-003",  # 您可以根據需要使用不同的模型
            prompt=essay,
            max_tokens=10000  # 根據 Render 的要求，可以設定 max_tokens
        )

        result = response.choices[0].text.strip()
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure it listens on all IPs and uses the PORT environment variable
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))  # Default to 5000 if no PORT is set
