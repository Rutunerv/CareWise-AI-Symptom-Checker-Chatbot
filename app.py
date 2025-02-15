from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure PaLM API (Replace 'YOUR_API_KEY' with your actual API key)
genai.configure(api_key="AIzaSyAiNxpUDhTfozcKUoARvbL38jwTTqxr-w8")

# Function to get diagnosis from PaLM
def get_diagnosis(symptoms):
    prompt = f"I have the following symptoms: {symptoms}. What could be the possible diagnosis?"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response.text else "I'm not sure. Please consult a doctor."

# API Route to receive symptoms and return diagnosis
@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    symptoms = data.get("symptoms", "")
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400
    diagnosis = get_diagnosis(symptoms)
    return jsonify({"diagnosis": diagnosis})

if __name__ == '__main__':
    app.run(debug=True)
