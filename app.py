from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)

# 從環境變數中讀取 OpenAI API 密鑰
openai.api_key = os.getenv('OPENAI_API_KEY')  # 從 .env 文件中獲取 API 密鑰

# 設置 /evaluate 路由來處理 POST 請求
@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        # 從前端接收文章
        essay = request.json.get('essay')

        # 發送請求到 OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # 使用 Davinci 引擎
            prompt=essay,
            max_tokens=200
        )

        # 取得結果並回傳
        feedback = response["choices"][0]["text"].strip()
        return jsonify({"result": feedback}), 200

    except Exception as e:
        # 捕捉錯誤並回傳
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 啟動 Flask 應用並設定為 debug 模式，讓它可以根據 render 的配置自動綁定端口
    app.run(debug=True, host="0.0.0.0")
