import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))  # server/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # root

from flask import Flask, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import cv2
import uuid
import time
import json
import requests
from io import BytesIO
from PIL import Image
import base64
import numpy as np
from utils.preprocess import preprocess_image
from dotenv import load_dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads')
app.config['CLOTHING_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'clothing_images') 
app.config['CLIENT_FOLDER'] = '../client'

# Load environment variables from .env file
load_dotenv()

# FASHN API configuration
FASHN_API_BASE = "https://api.fashn.ai/v1"
FASHN_API_KEY = os.getenv('FASHN_API_KEY')
assert FASHN_API_KEY, "FASHN_API_KEY not found in environment variables. Please check your .env file."

def encode_image_to_base64(image_data):
    return f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"

@app.route('/')
def serve_index():
    return send_from_directory(app.config['CLIENT_FOLDER'], 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.config['CLIENT_FOLDER'], path)

@app.route('/api/clothing', methods=['GET'])
def get_clothing():
    clothing_items = [
        {'id': '1', 'name': 'Ankara Dress', 'imageUrl': '/clothing_images/clothing_1.png', 'type': 'full'},
        {'id': '2', 'name': 'T-Shirt', 'imageUrl': '/clothing_images/clothing_2.png', 'type': 'upper'},
        {'id': '3', 'name': 'Formal Blazer', 'imageUrl': '/clothing_images/clothing_3.png', 'type': 'upper'},
        {'id': '4', 'name': 'Short Gown', 'imageUrl': '/clothing_images/clothing_4.png', 'type': 'upper'},
    ]
    return jsonify(clothing_items)

@app.route('/api/tryon', methods=['POST'])
def try_on():
    if 'customerImage' not in request.files or 'clothingId' not in request.form:
        return jsonify({'error': 'Missing customer image or clothing ID'}), 400

    customer_image = request.files['customerImage']
    clothing_id = request.form['clothingId']

    filename = secure_filename(customer_image.filename)
    customer_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(os.path.dirname(customer_path), exist_ok=True)
    customer_image.save(customer_path)
    print(f"Saved customer image to: {customer_path}")

    clothing_path = os.path.join(app.config['CLOTHING_FOLDER'], f'clothing_{clothing_id}.png')
    if not os.path.exists(clothing_path):
        print(f"Clothing image not found: {clothing_path}")
        return jsonify({'error': f'Clothing image not found: clothing_{clothing_id}.png'}), 400

    clothing_items = [
        {'id': '1', 'name': 'Ankara Top', 'imageUrl': '/clothing_images/clothing_1.png', 'type': 'full'},
        {'id': '2', 'name': 'T-Shirt', 'imageUrl': '/clothing_images/clothing_2.png', 'type': 'upper'},
        {'id': '3', 'name': 'Formal Blazer', 'imageUrl': '/clothing_images/clothing_3.png', 'type': 'upper'},
        {'id': '4', 'name': 'Short Gown', 'imageUrl': '/clothing_images/clothing_4.png', 'type': 'upper'},
    ]
    clothing_type = next(item['type'] for item in clothing_items if item['id'] == clothing_id)

    def generate():
        try:
            for i in range(10, 40, 10):
                time.sleep(0.5)
                yield f"data: {json.dumps({'progress': i})}\n\n"

            customer_img = preprocess_image(customer_path, is_clothing=False)
            _, customer_img_data = cv2.imencode('.png', customer_img)
            clothing_img = preprocess_image(clothing_path, is_clothing=True)
            _, clothing_img_data = cv2.imencode('.png', clothing_img)

            print(f"Customer image data length: {len(customer_img_data)} bytes")
            print(f"Clothing image data length: {len(clothing_img_data)} bytes")

            headers = {"Authorization": f"Bearer {FASHN_API_KEY}", "Content-Type": "application/json"}
            model_base64 = encode_image_to_base64(customer_img_data)
            garment_base64 = encode_image_to_base64(clothing_img_data)
            input_data = {
                "model_name": "tryon-v1.6",
                "inputs": {
                    "model_image": model_base64,
                    "garment_image": garment_base64
                }
            }
            print(f"Request data: model_image length: {len(model_base64)} bytes, garment_image length: {len(garment_base64)} bytes")

            run_response = requests.post(f"{FASHN_API_BASE}/run", json=input_data, headers=headers, timeout=30)
            if run_response.status_code != 200:
                error_msg = run_response.json().get('error', f'API error: {run_response.status_code}')
                yield f"data: {json.dumps({'error': error_msg, 'status': 'Failed'})}\n\n"
                return
            task_id = run_response.json().get('id')
            if not task_id:
                yield f"data: {json.dumps({'error': 'No task ID returned', 'status': 'Failed'})}\n\n"
                return
            print(f"Received task ID: {task_id}")

            max_polls = 40
            poll_interval = 2
            for attempt in range(max_polls):
                time.sleep(poll_interval)
                status_response = requests.get(f"{FASHN_API_BASE}/status/{task_id}", headers=headers, timeout=10)
                print(f"Status check attempt {attempt + 1}, response code: {status_response.status_code}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Raw status data: {status_data}")
                    clean_data = {k: (str(v).replace('\n', ' ') if isinstance(v, str) else v) for k, v in status_data.items()}
                    print(f"Cleaned status data: {clean_data}")
                    progress = clean_data.get('progress', 0)
                    yield f"data: {json.dumps({'progress': progress, 'status': clean_data.get('status')})}\n\n"
                    if clean_data.get('status') == 'completed':
                        output_url = clean_data.get('output', [None])[0]
                        if output_url:
                            response = requests.get(output_url, timeout=10)
                            if response.status_code == 200:
                                result_image_data = response.content
                                result_image = Image.open(BytesIO(result_image_data))
                                result_filename = f'result_{uuid.uuid4()}.png'
                                result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
                                os.makedirs(os.path.dirname(result_path), exist_ok=True)
                                result_image.save(result_path)
                                print(f"Result saved to: {result_path}")
                                yield f"data: {json.dumps({'resultImage': f'/uploads/{result_filename}', 'status': 'Complete'})}\n\n"
                            else:
                                yield f"data: {json.dumps({'error': f'Failed to fetch result image: {response.status_code}', 'status': 'Failed'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'error': 'No output URL in completed task', 'status': 'Failed'})}\n\n"
                        return
                    elif clean_data.get('status') == 'failed':
                        error_msg = clean_data.get('error', {}).get('message', 'Task failed')
                        yield f"data: {json.dumps({'error': error_msg, 'status': 'Failed'})}\n\n"
                        return
                else:
                    print(f"Status response: {status_response.text}")
                    if status_response.status_code in [401, 429]:
                        yield f"data: {json.dumps({'error': f'API error: {status_response.json().get("message", "Unknown error")}', 'status': 'Failed'})}\n\n"
                        return

            yield f"data: {json.dumps({'error': 'Task timed out. Please try again.', 'status': 'Failed'})}\n\n"

        except Exception as e:
            print(f"Error: {str(e)}")
            yield f"data: {json.dumps({'error': str(e), 'status': 'Failed'})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    with open('data/feedback.txt', 'a') as f:
        f.write(f"Score: {data['score']}, Comment: {data['comment']}\n")
    return jsonify({'status': 'success'})

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(os.path.dirname(app.config['UPLOAD_FOLDER']), filename)

@app.route('/clothing_images/<path:filename>')
def serve_clothing_image(filename):
    return send_from_directory(app.config['CLOTHING_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CLOTHING_FOLDER'], exist_ok=True)
    # app.run(debug=True)