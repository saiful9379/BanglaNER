

import os
import json
import requests
import time
from flask import Flask, request, jsonify
from inference import BanglaNER
from utils.model_downloading import download_file

root_dir = os.getcwd()

model_dir = os.path.join(root_dir, "models")

print("Downloading model ......")
model_dir = download_file(model_dir)



DEBUG = True


app = Flask(__name__)

bner = BanglaNER(model_dir)



@app.route('/ner', methods=['POST'])
def bangla_ner():
    """
    
    """
    st = time.time()
    data = request.get_json()
    sender = data.get('sender_id', '')
    text = data.get('text', '')

    print("request : ", request)

    print(f"sender : {sender}")
    print(f"text : {text}")

    prediction = bner.prediction(text)
    response = {
        "sender_id" : sender,
        "body"      : prediction,
        "status"    : 200
        }

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0",port=8008)