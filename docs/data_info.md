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


```B-PERSON``` means that the word ```"মো.``` is the beginning of a person, ```L-PERSON``` means that the word ```"বাদল"``` is inside a person and ```হোসেন``` is last name a person, ```O``` means that the word ```নামের``` is outside a named entity. U-PERSON means that "U-" often denotes a unit or unique instance of an entity.

