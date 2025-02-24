import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 設置 OpenAI API 密鑰
openai.api_key = '你的 OpenAI API 密鑰'

@app.route("/evaluate", methods=["POST"])
def evaluate_essay():
    data = request.get_json()
    essay = data.get("essay", "")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    try:
        # 發送請求給 OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",  # 這裡可以選擇你需要的模型
            prompt=essay,
            max_tokens=150
        )

        result = response.choices[0].text.strip()  # 獲取返回的文字
        return jsonify({"result": result})  # 返回結果

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)  # 修改端口為10000，與Render配置一致
