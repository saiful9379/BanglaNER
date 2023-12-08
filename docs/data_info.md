# Data information
Here the Bangla name entity recognition(NER) dataset is [IOB-tagging](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) format, which stands for Inside-Outside-Beginning.

__banglakit :  ```JSONL``` file of ```banglakit``` data example:__ 
```
 Text : "একই অভিযোগ করেন মো. বাদল হোসেন নামের আরেক পরীক্ষার্থী।", 
 
 IOB-tagging =  ["O", "O", "O", "B-PERSON", "I-PERSON", "L-PERSON", "O", "O", "O", "O"]
```

__Rifat1493_NER : ```TXT``` file of ```Rifat1493_NER``` data example:__ 
```txt
উন্নয়নের	O
বিস্ময়	O
বাংলাদেশ	B-LOC
বাংলাদেশের	B-LOC
অগ্রগতি	O
উদাহরণ	O
দেওয়ার	O
মতোই	O
।	O
```

__SemiEval : ```JSON``` file of ```Rifat1493_NER``` data example:__

```JSON
  {
    "id": 15298,
    "paragraphs": [
      {
        "sentences": [
          {
            "tokens": [
              {
                "orth": "ইয়ান",
                "tag": "-",
                "ner": "B-PER"
              },
              {
                "orth": "থমসন",
                "tag": "-",
                "ner": "L-PER"
              },
              {
                "orth": "এর",
                "tag": "-",
                "ner": "O"
              },
              {
                "orth": "বয়স",
                "tag": "-",
                "ner": "O"
              },
              {
                "orth": "কত",
                "tag": "-",
                "ner": "O"
              }
            ]
          }
        ]
      }
    ]
  }

```

Sentence like ```একই অভিযোগ করেন মো. বাদল হোসেন নামের আরেক পরীক্ষার্থী।```, then the corresponding tags would be ```["O", "O", "O", "B-PERSON", "I-PERSON", "L-PERSON", "O", "O", "O", "O"]```.


```B-PERSON``` means that the word ```"মো.``` is the beginning of a person, ```L-PERSON``` means that the word ```"বাদল"``` is inside a person and ```হোসেন``` is last name a person, ```O``` means that the word ```নামের``` is outside a named entity. U-PERSON mean that "U-" often denotes a unit or unique instance of an entity.

# Exploratory data analysis(EDA) NER DATA

Here bangla NER data  EDA of banglakit, Rifat1493, SemiEval dataset.


For More information please check below,

```
banglakit data processing report:

No. of Total Line                : 3545 
No. of Match Line with Label     : 3373
No. of Line Not Match with Label : 172

No. of Tokens :  67716

Label Frequency  {'O': 64908, 'B-PER': 1077, 'I-PER': 341, 'L-PER': 1077, 'U-PER': 313}
========================================================================================
Rifat1493 data processing report:

No. of Total Line : 6568
No. of Tokens :  96616
Label Frequency  {'O': 91303, 'B-PER': 2781, 'I-PER': 2532}
=======================================================================================

SemiEval data processing report:

No. of Lines    : 16098
No. of Tokens   : 202215
Label Frequency : {'O': 196155, 'B-PER': 2639, 'L-PER': 2639, 'I-PER': 672, 'U-PER': 110}
=========================================================================================

ALl Data Merged Data Report:

No. of Lines    : 26039
No. of Tokens   : 366547
Label Frequency : {'O': 352366, 'B-PER': 6497, 'I-PER': 3545, 'L-PER': 3716, 'U-PER': 423}

```
