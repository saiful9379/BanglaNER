```
(bangla_ner) sayan@sayan:/media/sayan/hdd/NLP/Hishab_assignment/BanglaNER$ bash train_cpu.sh 
✔ Created output directory: models/bangla_ner_model_v1
ℹ Saving to output directory: models/bangla_ner_model_v1
ℹ Using CPU
ℹ To switch to GPU 0, use the option: --gpu-id 0

=========================== Initializing pipeline ===========================
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['tok2vec', 'ner']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS NER  ENTS_F  ENTS_P  ENTS_R  SCORE 
---  ------  ------------  --------  ------  ------  ------  ------
  0       0          0.00     38.33    3.92    3.09    5.35    0.04
  0     200         11.90   2107.91   52.16   58.71   46.92    0.52
  0     400         10.39   1396.27   62.08   68.53   56.74    0.62
  0     600         12.58   1522.44   68.69   73.48   64.50    0.69
  1     800         14.92   1004.61   68.54   68.48   68.60    0.69
  2    1000         53.50   1112.00   74.19   76.74   71.81    0.74
  2    1200         75.47    897.78   75.89   79.69   72.44    0.76
  3    1400         26.08    866.35   75.00   82.08   69.05    0.75
  4    1600         33.77    783.12   76.47   78.86   74.22    0.76
  6    1800         38.83    776.47   77.35   79.73   75.11    0.77
  7    2000         46.71    766.76   77.50   81.85   73.60    0.78
  9    2200         46.42    807.94   77.55   83.68   72.26    0.78
 12    2400        236.76    853.79   77.29   81.71   73.33    0.77
 14    2600         69.87    852.63   77.11   81.31   73.33    0.77
 17    2800        583.80    826.48   77.36   83.25   72.26    0.77
 19    3000        109.35    759.07   77.15   83.11   71.99    0.77
 22    3200         64.72    733.21   77.64   81.82   73.86    0.78
 25    3400         45.29    713.10   77.74   82.27   73.68    0.78
 27    3600         70.92    697.45   77.18   83.42   71.81    0.77
 30    3800         90.63    695.76   77.02   81.21   73.24    0.77
 32    4000        125.35    717.56   77.96   81.78   74.49    0.78
 35    4200         39.69    650.39   78.99   82.86   75.47    0.79
 37    4400         68.10    689.83   77.83   81.06   74.84    0.78
 40    4600        602.25    700.51   77.65   81.41   74.22    0.78
 42    4800        287.62    645.62   76.00   81.87   70.92    0.76
 45    5000        212.55    649.40   77.28   81.57   73.42    0.77
 47    5200        222.54    644.51   76.19   82.30   70.92    0.76
 50    5400        239.63    626.73   76.67   79.69   73.86    0.77
 52    5600        651.96    677.29   73.66   82.20   66.73    0.74
 55    5800        763.62    675.25   73.36   84.44   64.85    0.73
✔ Saved pipeline to output directory
models/bangla_ner_model_v1/model-last

```
