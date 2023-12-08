# Bangla NER(Spacy) model Training using Transformer Based pipeline


# Hyperparamer Tunning
```
Bert Pretrain model = "csebuetnlp/banglabert"
window = 256
batch_size = 256

```

# Data Label Format

For the training NER model, used here span based annotation that means entity are label ```starting``` and ```ending``` position.

Example:

```
{"text": ": আল স্কিনিয়ার গিটার, পিয়ানো, ভোকাল, মগ সিনথেসাইজার", "label": [[2, 15, "PER"]]}
{"text": "সে একটি পাওয়ার জন্য এতটাই মরিয়া যে সে মিথ্যাভাবে বলে যে ব্যাগটি তার সেলিব্রিটি ক্লায়েন্টের জন্য লুসি লিউ ।", "label": [[99, 107, "PER"]]}

```


# Training logs
```
(bangla_ner) sayan@sayan:/media/sayan/hdd/NLP/Hishab_assignment/BanglaNER$ bash train_gpu.sh
✔ Created output directory: bangla_ner_model_v4
ℹ Saving to output directory: bangla_ner_model_v4
ℹ Using GPU: 0

=========================== Initializing pipeline ===========================
Some weights of the model checkpoint at csebuetnlp/banglabert were not used when initializing ElectraModel: ['discriminator_predictions.dense.bias', 'discriminator_predictions.dense_prediction.weight', 'discriminator_predictions.dense.weight', 'discriminator_predictions.dense_prediction.bias']
- This IS expected if you are initializing ElectraModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing ElectraModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['transformer', 'ner']
ℹ Initial learn rate: 0.0
E    #       LOSS TRANS...  LOSS NER  ENTS_F  ENTS_P  ENTS_R  SCORE 
---  ------  -------------  --------  ------  ------  ------  ------
  0       0        1431.57    584.42    8.00    5.51   14.60    0.08
  0     200       41363.02  45560.27   86.08   88.32   83.95    0.86
  1     400        4447.77   5595.73   91.36   89.97   92.80    0.91
  1     600        3391.38   4310.18   92.98   92.77   93.18    0.93
  2     800        2907.31   3575.17   94.13   94.61   93.65    0.94
  2    1000        2492.62   3069.12   94.92   94.73   95.11    0.95
  3    1200        2089.18   2579.18   95.52   95.57   95.47    0.96
  3    1400        2187.35   2612.57   96.08   96.83   95.33    0.96
  4    1600        1737.86   2098.58   96.39   96.25   96.52    0.96
  5    1800        1740.79   2082.19   96.53   97.04   96.02    0.97
  5    2000        1598.81   1864.84   96.77   96.29   97.25    0.97
  6    2200        1498.09   1773.07   96.80   97.05   96.56    0.97
  6    2400        1476.27   1747.88   97.04   97.34   96.75    0.97
  7    2600        1232.35   1442.20   97.10   97.06   97.15    0.97
  7    2800        1352.76   1597.02   97.30   96.68   97.93    0.97
  8    3000        1182.07   1363.52   97.26   97.11   97.41    0.97
  9    3200        1253.93   1451.76   97.34   96.87   97.82    0.97
  9    3400        1336.89   1391.70   97.34   97.64   97.05    0.97
 10    3600        1510.68   1335.80   97.42   97.26   97.59    0.97
 10    3800        1108.69   1282.33   97.35   97.70   97.00    0.97
 11    4000        1068.47   1271.26   97.24   95.88   98.64    0.97
 11    4200        1031.50   1251.79   97.50   96.55   98.46    0.97
 12    4400         990.43   1197.36   97.46   97.36   97.56    0.97
 13    4600        1038.73   1261.60   97.45   98.26   96.65    0.97
 13    4800         928.43   1117.48   97.52   96.97   98.08    0.98
 14    5000         989.37   1221.82   97.52   97.27   97.78    0.98
 14    5200         986.62   1196.29   97.56   96.92   98.22    0.98
 15    5400         879.36   1090.96   97.54   96.92   98.17    0.98
 15    5600         918.28   1162.04   97.43   98.97   95.95    0.97
 16    5800         899.11   1129.42   97.51   96.80   98.22    0.98
 17    6000         903.24   1094.54   97.46   97.27   97.65    0.97
 17    6200         871.53   1122.06   97.53   97.04   98.03    0.98
 18    6400         891.70   1095.20   97.45   98.61   96.33    0.97
 18    6600        1083.30   1125.82   97.57   96.68   98.48    0.98
 19    6800         931.69   1073.05   97.49   98.70   96.32    0.97
 19    7000         821.91   1086.37   97.57   97.20   97.94    0.98
 20    7200         833.46   1061.53   97.62   96.99   98.26    0.98
 21    7400         786.92   1060.68   97.60   97.00   98.20    0.98
 21    7600         815.66   1101.18   97.62   97.03   98.22    0.98
 22    7800         757.33    993.51   97.62   97.12   98.12    0.98
 22    8000         738.43    995.63   97.59   97.22   97.97    0.98
 23    8200         828.81   1099.15   97.53   98.95   96.15    0.98
 23    8400         878.53   1043.72   97.49   99.06   95.98    0.97
 24    8600         856.89   1055.40   97.50   99.14   95.91    0.97
 25    8800         777.17   1039.05   97.61   97.19   98.04    0.98
✔ Saved pipeline to output directory
bangla_ner_model_v4/model-last


```