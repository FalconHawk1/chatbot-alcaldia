from flask import Flask, request, jsonify
import openai

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key (Replace with your actual key)
openai.api_key = os.getenv("OPENAI_API_KEY")

#"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"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    # Send the user message to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en Pokémon."},
            {"role": "user", "content": user_message}
        ]
    )
    
    # Get the response content
    gpt_response = response["choices"][0]["message"]["content"]
    
    return jsonify({"response": gpt_response})

if __name__ == "__main__":
    app.run(debug=True)
