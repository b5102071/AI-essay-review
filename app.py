from flask import Flask, render_template, request, jsonify
import openai
import os  # 新增這行來讀取環境變數

app = Flask(__name__)

# 使用環境變數讀取 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# 隱藏指令
SYSTEM_MESSAGE = """
You are an expert in English writing evaluation. Based on the given topic, guidelines, and the following scoring criteria, you must provide a score and detailed suggestions for improvement. Then, rewrite the article into a refined version that aligns with the suggestions while maintaining a level achievable by the user. If the transitions between ideas or sentences, or the narrowing down in the introductory part, are weak, provide examples for improvement. Identify any traces of Chinese thinking and offer revision suggestions. Also, check the use of tenses, ensuring that transitions between ideas are properly executed, and provide further recommendations if needed. 

Lastly, provide a sentence-by-sentence revision.

Scoring Criteria (Total: 20 points):
- **Content (30%)**: Assess topic relevance, clarity of theme, and supporting details.
- **Organization (25%)**: Evaluate logical structure, paragraph divisions, smooth transitions, coherence, and cohesion.
- **Language Use (30%)**: Assess variety in sentence structures, vocabulary diversity, accuracy, fluency, and grammatical correctness.
- **Spelling and Punctuation (15%)**: Ensure correct spelling and proper punctuation.

After scoring and providing suggestions, identify the user's spelling and grammatical errors. Then, generate practice exercises based on these mistakes.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    essay = request.form['essay']
    
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"Here is my essay:\n\n{essay}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    return jsonify({"response": response["choices"][0]["message"]["content"]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
