from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, template_folder='templates')  # Look for templates in "templates" folder

# Setup Google Gemini API
def setup_client():
    api_key = "AIzaSyAYSDaesTR47kukyiHoYwGC6hsPnNxpOuY"  # Replace with a valid API key
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

try:
    model = setup_client()
    print("Successfully initialized Gemini API")
except Exception as e:
    print(f"Error setting up Gemini API: {str(e)}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')  # Make sure "index.html" is inside "templates" folder

@app.route('/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"error": "AI model not initialized. Please check your API key."}), 500

    data = request.get_json()
    user_message = data.get('message') if data else None

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Generate response using Gemini
        response = model.generate_content(
            user_message,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 800
            }
        )

        # Extract the generated text
        if response.text:
            return jsonify({"response": response.text.strip()})
        else:
            return jsonify({"error": "No response generated"}), 500

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
