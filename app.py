from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 確保 OpenAI API 金鑰設定正確
openai.api_key = os.getenv("OPENAI_API_KEY")

# 根路徑處理
@app.route('/')
def home():
    return "Welcome to AI Essay Review! Your service is up and running."

# 評估路由
@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.get_json()  # 從前端獲取 JSON 請求體
        essay = data.get("essay")
        if not essay:
            return jsonify({"error": "No essay provided"}), 400  # 如果沒有提供 essay，回傳 400 錯誤

        # 呼叫 OpenAI API 來生成評估，將 max_tokens 設為 10000
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Please evaluate this essay:\n\n{essay}",
            max_tokens=10000  # 設定 max_tokens 為 10000
        )

        # 嘗試從 API 回應中提取評估結果
        try:
            feedback = response["choices"][0]["text"].strip()  # 提取評估結果
            return jsonify({"feedback": feedback})  # 回傳 JSON 格式的評估結果
        except KeyError as e:
            return jsonify({"error": f"KeyError: {str(e)}"}), 500  # 如果解析回應時出錯，回傳 500 錯誤
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500  # 其他未知錯誤

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # 捕捉任何一般錯誤

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # 這樣 Flask 會根據 Render 的設定來分配端口
