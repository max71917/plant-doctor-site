from http.server import BaseHTTPRequestHandler
   import json
   import base64
   from openai import OpenAI
   import os

   class handler(BaseHTTPRequestHandler):
       def do_POST(self):
           content_length = int(self.headers.get('Content-Length', 0))
           body = self.rfile.read(content_length)
           data = json.loads(body)
           
           image_base64 = data.get('image')
           
           client = OpenAI(
               api_key=os.environ.get('API_KEY'),
               base_url=os.environ.get('BASE_URL')
           )
           
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
           
           answer = response.choices[0].message.content
           
           self.send_response(200)
           self.send_header('Content-Type', 'application/json')
           self.send_header('Access-Control-Allow-Origin', '*')
           self.end_headers()
           self.wfile.write(json.dumps({'answer': answer}).encode())
