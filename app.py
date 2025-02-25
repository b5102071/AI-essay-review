import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    essay = data.get("essay")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    try:
        # Use OpenAI to analyze the essay, setting max_tokens to 10000
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use a different model if needed
            prompt=essay,
            max_tokens=10000  # Set max_tokens based on your requirements
        )

        result = response.choices[0].text.strip()
        return jsonify({"result": result})

    except openai.error.OpenAIError as e:
        # Catch OpenAI API errors and return the error message
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    except Exception as e:
        # Catch any other errors and return the error message
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  # Default to 5000 for local testing
    app.run(debug=True, host="0.0.0.0", port=int(port))
