# Bangla_NER

Bangla Name Entity Recognition (NER) is extracting human names from input Bangla string or text. To solve this problem here try 2 pipelines such as [Spacy](https://spacy.io/) pipeline as well as [BERT](https://en.wikipedia.org/wiki/BERT_(language_model)) model and try 5 experimental approaches. 

The experiment is done only using one entity name (person) labeled as PER. After completing the experiment we got the best performance from the spacy transformer-based model.

For more detail please check the experimental detail and F1 score in experimental history. Where best F1-score is ~.81.05 [check](docs/experiemts.md). 


# Installation

```
conda create -n bn_ner python=3.8
pip install -r requirements.txt
```

N.B:  if raise  ```CuPy``` error, install ```pip install CuPy==12.3.0``` version for GPU acceleration.

# Dataset

## Data Collection Information

Bangla NER data is collected from,

1. banglakit Bangla NER Dataset [Link](https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl)

2. Rifat1493 Bangla NER Dataset [Link](https://github.com/Rifat1493/Bengali-NER/tree/master/Input) 


3. SemEval2022 Bangla NER Dataaset [Link](https://competitions.codalab.org/competitions/36425#learn_the_details)




raw dataset structure into ```raw_data``` folder,

```
raw_data
├── banglakit
│   └── main.jsonl
├── Rifat1493_NER_txt
│   └── all_data.txt
└── SemiEval
    ├── bn_dev.json
    ├── bn_train.json
    └── statistics.md
```

## Dataset Annotation Information

For more information about Bangla NER data please check [check](docs/data_info.md)

## Data Processing

Please check the data processing approach [check](docs/data_processing)




# Model Building

## Training Spacy Pipeline

Please check more details training strategy and spacy model training procedure please [check](docs/spacy.md) or colab training
click the colab icon.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1YU7WXkpdwwmFSwPtZGuzlKgntqmZlALF)

## BERT


Not yet complete


# Evaluation

| Model Name | Model Type | Approch | Dataset | Precision | Recall | F-Score |
| ------------- | ------------- | --------    |--------    | ------------- | ------------- | --------    |
Spacy   | Default(CPU)  |BLIOU  | Train :___, val:__ | 39 M 	| X |  X
Spacy   | Default(CPU)  |Docanno  | Training : | 99.01%| 77.39%| 86.88%
Spacy   | Default(CPU)  |Docanno  | Training : | 99.01%| 77.39%| 86.88%
Spacy  | Default(CPU)  |Docanno  | Training : | 99.01%| 77.39%| 86.88%
Spacy | Default(CPU)  |Docanno  | Training : | 99.01%| 77.39%| 86.88%
large  | Default(CPU)  |Docanno  | Training : | 99.01%| 77.39%| 86.88%

# Inference

For the inference, run ```inference.py``` script the model will download automatically from huggingface and be stored in the "models" folder. After download, it will unzip also.

if have any issues with the model downloading, please download manually from [here](https://huggingface.co/saiful9379/BanglaNER/tree/main)

run,

```py
pyhton inference.py
```


Code Example,
```py
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("models/bangla_ner_model/model-best")

text_list = [
    "আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম",
    "নতুন বছরে জ্বলছেন আরও একজন—রজার ফেদেরার ।",
    "ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান",
    "তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।",
    "লিশ ট্র্যাক তৈরির সময় বেশ কয়েকজন শিল্পীর দ্বারা অনুপ্রাণিত হওয়ার কথা স্মরণ করেন, বিশেষ করে ফ্রাঙ্ক সিনাত্রা ।",
]
for text in text_list:
    doc = nlp(text)
    print(f"Input: {text}")
    for entity in doc.ents:
        print(f"Entity: {entity.text}, Label: {entity.label_}")
    print("---")

```
__Ouptut__

```sh
Input: আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম
Entity: আব্দুর রহিম, Label: PER
---
Input: নতুন বছরে জ্বলছেন আরও একজন—রজার ফেদেরার ।
---
Input: ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান
Entity: মুনীর চৌধুরী, Label: PER
---
Input: তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।
Entity: মোহাম্মদ বাকির আল-সদর, Label: PER
---
Input: লিশ ট্র্যাক তৈরির সময় বেশ কয়েকজন শিল্পীর দ্বারা অনুপ্রাণিত হওয়ার কথা স্মরণ করেন, বিশেষ করে ফ্রাঙ্ক সিনাত্রা ।
Entity: ফ্রাঙ্ক সিনাত্রা, Label: PER
```
Or 

inference notebook [check](training/example/interence.ipynb)

# Docker

## Docker install

For docker install please [check](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)


## Docker Build

```
sudo docker build -t bangla_ner .
```
Check the Docker image and image ID,

```
sudo docker images
```
Output,
```sh
REPOSITORY      TAG                                 IMAGE ID       CREATED          SIZE
bangla_ner      latest                              c34a96d16f48   4 minutes ago    ...GB

```

For cpu run,

```sh
# run it first
sudo docker run -it -p 5000:5000 bangla_ner /bin/bash
# go inference directory
cd inference/
# run 
python3 app.py
```
After running app file output show ip-address looks like this,

```sh
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8008
 * Running on http://172.17.0.2:8008
```
__N.B: For inside the docker inference, Take the last ip and change the ```End Point API``` request url ```http://localhost:8008/ner"``` using this ```http://172.17.0.2:8008```. this are only when the application run inside docker. otherwise no need to change ```End Point API```__ 



# End Point API

Some instruction as inference section. run ```app.py``` model will download and the server will run also.

For more details about API requests, please [check](docs/end_point.md)

# Reference

1. [Spacy Training Pipelines & Models](https://spacy.io/usage/training)
2. [NER data annotation](https://doccano.github.io/doccano/tutorial/)

3. [BERT Pretrin model ](https://github.com/csebuetnlp/banglabert)
4. [BILOU data formats meaning](https://stackoverflow.com/questions/17116446/what-do-the-bilou-tags-mean-in-named-entity-recognition)
5. [SpaCy 3.1 data format](https://zachlim98.github.io/me/2021-03/spacy3-ner-tutorial)
6. [Tranformer infornation](https://jalammar.github.io/illustrated-transformer/)
7. [Load Gensim WordVectors into spacy pipeline](https://stackoverflow.com/questions/75521069/load-gensim-wordvectors-into-spacy-pipeline)
8. [Postman ](https://www.postman.com/)
9. [curl request](https://curl.se/docs/httpscripting.html)





