import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return "Welcome to AI Essay Review!"

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        # Get the essay text from the POST request
        essay = request.form['essay']
        
        # Call the OpenAI API for evaluation
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Please review the following essay:\n{essay}\nProvide feedback and suggestions for improvement.",
            max_tokens=500
        )
        
        # Extract feedback from the response
        feedback = response["choices"][0]["text"].strip()
        
        # Return the feedback as JSON
        return jsonify({"result": feedback})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app with debug mode enabled
    app.run(debug=True, host="0.0.0.0")
