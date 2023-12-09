# Bangla_NER

Bangla Name Entity Recognition (NER) is extracting human names from input Bangla string or text. To solve this problem here select [Spacy](https://spacy.io/) pipeline and try 5 experimental approaches. 

The experiment is done only using one entity name (person) labeled as PER. After completing the experiment we got the best performance from the spacy transformer-based model.

For more detail please check the [experimental details](docs/experiemts.md) and Best model F1 score is ~.81.05. 


# Installation

```
conda create -n bn_ner python=3.8
pip install -r requirements.txt
```

N.B:  if raise  ```CuPy``` error, install ```pip install CuPy==12.3.0``` version for GPU acceleration.

# Dataset

Check the ```training/utils``` folder for Data processing script. 

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


Data processing approach,


1. Raw Data Processing
2. Span Based Data Processing(Doccano NER format)
3. Preparing Training Spacy Format
4. Augment Data generation
5. Summary Report


<!-- This [IOB-tagging](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) dataset needs to filter because some lines match with its label and some do not match. -->
## 1. Raw Data Processing
Raw data processing steps:

    1. Exclude other classes without PERSON Class(PER)

    2. Discard the dataset not matching with label

    3. Clean IOB and remove data that is in the wrong IOB format

    5. Minimal data remove which is logically valid and matching token.  

    6. BLIOU Annotation checking and correction

    7. Data Distribution training (80%) and validation (20%)

    8. Randomly data shuffle - 4 times

Get for information about ```BLIOU``` format please check [Example](https://github.com/explosion/spaCy/blob/v2.3.5/examples/training/ner_example_data/ner-token-per-line.json)


For those processing please check the script ```utils/data_processing.py``` line number ```443``` to ```445``` dataset path directory, 

__input__:
```sh
# make sure the input dataset path
banglakit= "./data/raw_data/banglakit/main.jsonl"
rifat1493 = "./data/raw_data/Rifat1493_NER_txt/all_data.txt"
semieval = "./data/raw_data/SemiEval"

```

Register the data line number ```453```,

``` sh
register_dataset = {
    "BanglakitNER"   : banglakit,
    "Rifat1493BnNER" : rifat1493,
    "SemiEvalBnNER"  : semieval_files
}
```

__N.B: if any dataset is not possible to collect avoid the data into the register field. data will be processed which have registered.__


Run
```
python utils/data_processing.py

```
Output,
```sh
No. of Training data : 20831
No. of Validation data : 5208

```
__Data Save directory__,

```sh
data
└── ner_bliou_processed_data
    ├── train.json
    └── val.json
```

__1. EDA Report__

![](image/eda.png)

## 2. Span-Based Data Processing(Doccano NER format)

For the Doccano annotation format please check [link](https://doccano.github.io/doccano/tutorial/)

Make sure input and output path directory into script ```python utils/conversion_bliou_to_span_format.py```line number ```201```,

```sh
#make sure input path directory
data_path = "./data/ner_bliou_processed_data"
#make sure output path directory  
output_dir = "./data/ner_spanbased_process_data"
```

output : 
``` sh
processed file : ./data/ner_spanbased_process_data/train.jsonl
Total number of line : 20831
Person Tag Found  : 4483

processed file : ./data/ner_spanbased_process_data/val.jsonl
Total number of line : 5208
Person Tag Found  : 1161
```



## 3. Preparing Training Spacy Format

For convet data to spacy format make sure data path into script ```utils/conversion_spacy_format.py```,

``` sh
# input path dir
input_dir = "./data/ner_spanbased_process_data"
# output path dir
output_dir = "./data/ner_spanbased_process_data"
```


Output:
``` sh

# convert train data to spacy format and save dir
Spacy Processed file   : ./data/ner_spanbased_process_data/train.spacy
No. of Processed line : 4483
# None span found 
No. of Skip Entity  : 11

# convert val data to spacy format and save dir
Spacy Processed file   : ./data/ner_spanbased_process_data/val.spacy
No. of Processed line : 1146
# None span found
No. of Skip Entity  : 3
```

check the annotation visualization [notebook](../training/example/data_annotation_visulization.ipynb)

Now the .spacy file processing process is complete, we can train spacy ner pipeline using .spacy file




N.B : if you want to train the spacy ner pipeline model using BLIOU format data run below the command,

```sh
Data conversion command for BLIOU, Convert `BLIOU` json format to `.spacy` data format

python -m spacy convert data/bangla_ner_data/train.json ./data
python -m spacy convert data/bangla_ner_data/val.json ./data

```

## 4. Augment Data generation

- Scraping human name data from several website
- Replace the name into text using span position and update the IOU span of the text.


## 5. Data Processing Summary

Here the report present dataset information, it processing data and exclude data which are not resolve using valid logic. 



__1. Data Summary__
![](image/data_summary.png)



# Model Building

## Training Spacy Pipeline

Please check more details training strategy and spacy model training procedure please [check](docs/spacy.md) or colab training
click the colab icon.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1YU7WXkpdwwmFSwPtZGuzlKgntqmZlALF)


# Evaluation

__Model Performance Summary__

![](./image/model_summary.png)

For more detaild check [report](./report/Bangla_NER_report_20231209.xlsx)



# Inference

For the inference, run ```inference.py``` script the model will download automatically from huggingface and be stored in the "models" folder. After download, it will unzip also.

if have any issues with the model downloading, please download manually from [here](https://huggingface.co/saiful9379/BanglaNER/tree/main)

run,

```py
pyhton inference.py
```
Or Check the colab for instance inference,



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uN1WP7MjaBYXKABfhkHGn7EBWm9kd9k9?usp=sharing)




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





