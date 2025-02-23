import os
import openai
from flask import Flask, request, jsonify, render_template

# 確保 Flask 應用程序正確設置
app = Flask(__name__)

# 從環境變數讀取 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        data = request.json
        essay_text = data.get("essay", "")

        if not essay_text:
            return jsonify({"error": "No essay provided"}), 400

        # OpenAI API 請求
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in essay evaluation. Provide feedback on grammar, coherence, and structure."},
                {"role": "user", "content": f"Please evaluate the following essay:\n\n{essay_text}"}
            ]
        )

        feedback = response.choices[0].message.content
        return jsonify({"feedback": feedback})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
