from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# 確保 OpenAI API 金鑰設定正確
openai.api_key = os.getenv("OPENAI_API_KEY")

# 根路徑處理，顯示表單
@app.route('/')
def home():
    return render_template('index.html')

# 評估路由，處理表單提交
@app.route('/evaluate', methods=['POST'])
def evaluate():
    essay = request.json.get('essay')  # 從 POST 請求中獲取作文
    if not essay:
        return jsonify({"error": "No essay provided"}), 400  # 如果沒有提供 essay，回傳錯誤

    try:
        # 呼叫 OpenAI API 來生成評估
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Please evaluate this essay:\n\n{essay}",
            max_tokens=10000
        )
        feedback = response["choices"][0]["text"].strip()
        return jsonify({"feedback": feedback})  # 回傳評估結果

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 捕捉並回傳錯誤

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # 這樣 Flask 會根據 Render 的設定來分配端口
