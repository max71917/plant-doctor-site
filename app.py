from flask import Flask, request, jsonify, send_from_directory
import base64
from openai import OpenAI
import os

app = Flask(__name__, static_folder='.', static_url_path='')

client = OpenAI(
    api_key=os.environ.get('API_KEY'),
    base_url=os.environ.get('BASE_URL')
)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_base64 = data.get('image')
    
    response = client.chat.completions.create(
        model=os.environ.get('MODEL', 'am/minimax-m3'),
        messages=[
            {"role": "system", "content": "Ты агроном. Определи: 1. Растение, 2. Диагноз, 3. Лечение. Отвечай на русском кратко."},
            {"role": "user", "content": [
                {"type": "text", "text": "Что за болезнь?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}
        ],
        max_tokens=1000
    )
    
    return jsonify({'answer': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
