## Data Processing

Data processing approach,


1. Raw Data Processing
2. Span Based Data Processing(Doccano NER format)
3. Preparing Training Spacy Format

<!-- This [IOB-tagging](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) dataset needs to filter because some lines match with its label and some do not match. -->
## 1. Raw Data Processing
Raw data processing steps:

    1. Exclude other classes without PERSON Class(PER)

    2. Discard the dataset not matching with label

    3. Clean IOB and remove data that is in the wrong IOB format

    4. BLIOU Annotation checking and correction

    5. Data Distribution training (80%) and validation (20%)

    6. Randomly data shuffle - 4 times

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

Data processing BLIOU Format Run,
```
python utils/data_processing.py

```
BLIOU Data Distribution Output,
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
processed file : ./data/ner_spanbased_process_data/val.jsonl
Total number of line : 5208
Person Entity Found Line : 1161
processed file : ./data/ner_spanbased_process_data/train.jsonl
Total number of line : 20831
Person Entity Found Line : 4483
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
No. of Processed line : 4447
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

# Output
✔ Generated output file (26039 documents): data/train.spacy
✔ Generated output file (999 documents): data/val.spacy
```
