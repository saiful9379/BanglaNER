# Bangla NER(Spacy) model Training pipeline

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DZbFzB3V6I1fueIQxDfxGhW11_m8LVtq)



# Data Label Format

For the training NER model, used here span based annotation that means entity are label ```starting``` and ```ending``` position.

Example:

```
{"text": ": আল স্কিনিয়ার গিটার, পিয়ানো, ভোকাল, মগ সিনথেসাইজার", "label": [[2, 15, "PER"]]}
{"text": "সে একটি পাওয়ার জন্য এতটাই মরিয়া যে সে মিথ্যাভাবে বলে যে ব্যাগটি তার সেলিব্রিটি ক্লায়েন্টের জন্য লুসি লিউ ।", "label": [[99, 107, "PER"]]}

```


# Training logs
```
✔ Created output directory: models/bangla_ner_model_v5
ℹ Saving to output directory: models/bangla_ner_model_v5
ℹ Using GPU: 0

=========================== Initializing pipeline ===========================
Some weights of the model checkpoint at csebuetnlp/banglabert were not used when initializing ElectraModel: ['discriminator_predictions.dense_prediction.bias', 'discriminator_predictions.dense_prediction.weight', 'discriminator_predictions.dense.bias', 'discriminator_predictions.dense.weight']
- This IS expected if you are initializing ElectraModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing ElectraModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['transformer', 'ner']
ℹ Initial learn rate: 0.0
E    #       LOSS TRANS...  LOSS NER  ENTS_F  ENTS_P  ENTS_R  SCORE 
---  ------  -------------  --------  ------  ------  ------  ------
  0       0         225.68    225.81   12.66    8.28   26.88    0.13
  2     200       30807.47  37485.75   87.74   84.97   90.69    0.88
  5     400        2795.52   3430.28   95.15   95.84   94.47    0.95
  7     600        1454.26   1731.12   97.30   97.41   97.20    0.97
  9     800        1114.09   1266.72   97.94   98.71   97.18    0.98
 12    1000         878.39    918.37   98.19   99.45   96.97    0.98
 14    1200         752.95    803.09   98.29   99.22   97.38    0.98
 17    1400         680.16    709.60   98.42   99.18   97.66    0.98
 19    1600         702.71    724.96   98.40   99.54   97.29    0.98
 22    1800         637.97    671.87   98.51   99.04   97.98    0.99
 24    2000         618.16    636.80   98.50   99.53   97.50    0.99
 27    2200         613.11    620.88   98.49   99.84   97.18    0.98
 29    2400         595.97    614.21   98.49   99.47   97.52    0.98
 31    2600         663.77    646.61   98.54   99.12   97.97    0.99
 34    2800         598.30    587.27   98.54   99.69   97.41    0.99
 36    3000         598.08    596.02   98.55   99.03   98.07    0.99
 39    3200         572.33    570.28   98.54   99.45   97.65    0.99
 41    3400         572.98    568.78   98.55   99.62   97.50    0.99
 44    3600         593.39    581.05   98.55   99.74   97.38    0.99
 46    3800         600.35    582.55   98.55   99.74   97.38    0.99
 49    4000         571.26    549.44   98.55   99.37   97.75    0.99
 51    4200         607.95    582.20   98.51   98.59   98.43    0.99
 54    4400         604.85    589.12   98.56   99.13   97.98    0.99
 56    4600         593.43    575.42   98.56   99.80   97.36    0.99
 59    4800         539.08    511.54   98.58   99.49   97.68    0.99
 61    5000         575.65    541.76   98.53   99.33   97.75    0.99
 64    5200         575.80    548.14   98.52   98.75   98.29    0.99
 66    5400         562.39    534.49   98.55   98.82   98.29    0.99
 68    5600         581.99    557.93   98.58   99.56   97.61    0.99
 71    5800         561.46    532.72   98.57   98.80   98.34    0.99
 73    6000         571.92    538.98   98.58   99.46   97.72    0.99
 76    6200         555.74    522.94   98.41   98.62   98.20    0.98
 78    6400         596.40    531.80   98.55   98.83   98.27    0.99
 81    6600         592.02    546.26   98.57   99.51   97.65    0.99
 83    6800         538.43    506.44   98.58   99.67   97.50    0.99
 85    7000         548.30    514.35   98.54   99.54   97.56    0.99
 88    7200         574.97    518.61   98.54   99.69   97.41    0.99
 90    7400         565.96    512.37   98.47   99.65   97.31    0.98
 93    7600         585.34    536.99   98.56   99.65   97.48    0.99
✔ Saved pipeline to output directory
models/bangla_ner_model_v5/model-last


```