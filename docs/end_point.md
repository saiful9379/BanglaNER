# API Request
For API-based testing run ```app.py``` script and open Postman, and send the post request using the below request body.


# Python payload,

``` py
url = "http://localhost:8008/ner"
payload = {
    "text" : "তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।",
    "sender_id" : "saiful"
}
headers = {'content-type': 'application/json'}
    result = requests.post(
        url, 
        json=payload, 
        headers=headers
    )
response = result.json()
# print("response : ", response)
return response

```

# CURL Request,

Install curl for API requests,

```
sudo apt  install curl
```

```
curl localhost:8008/ner -d '{"text" : "তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।", "sender_id" : "saiful"}' -H 'Content-Type: application/json'
```


# Postman request URL,
```py
# set post request and give this URL
http://localhost:8008/ner

{"text" : "তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।", "sender_id" : "saiful"}

```


Output,

```
{
    "body": {
        "0": {
            "cls": "PER",
            "person_name": "মোহাম্মদ বাকির আল-সদর",
            "span_position": [
                5,
                26
            ]
        }
    },
    "sender_id": "saiful",
    "status": 200
}
```
