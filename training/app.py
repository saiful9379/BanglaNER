

import os
import json
import requests
import time
from flask import Flask, request, jsonify


from inference import BanglaNER

DEBUG = True


app = Flask(__name__)
class config:
    model_path = "./models/bangla_ner_model"

cfg = config()
bner = BanglaNER(cfg.model_path)



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