from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_message = get_response(user_message)
    return jsonify({'response': response_message})

def get_response(message):
    message = message.lower()
    if 'hello' in message or 'hi' in message:
        return 'Hello! How can I help you today?'
    elif 'bye' in message or 'goodbye' in message:
        return 'Goodbye! Have a great day!'
    elif 'who are you' in message:
        return 'I am just a bot, but I am functioning properly. How about you?'
    elif 'your name' in message:
        return 'I am a simple chatbot created to assist you. What is your name?'
    elif 'weather' in message:
        return 'I am not able to provide live weather updates at the moment. Please check your favorite weather website.'
    elif 'time' in message:
        return 'I am not equipped to tell the time. Please check your device for the current time.'
    elif 'help' in message:
        return 'I am here to help! You can ask me about various topics like greetings, weather, and more.'
    else:
        return 'I am not sure how to respond to that. Can you please rephrase?'

if __name__ == '__main__':
    app.run(debug=True)
