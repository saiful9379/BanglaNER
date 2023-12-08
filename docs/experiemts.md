# Experiment Summary 


# Experiment - 1
    1. Data cleaning and convet the data BLIOU format
    2. Correction BLIOU format and EDA
    3. Convert BLIOU format data to doccano span-based format
    4. Data distribution training and validation:
        - Training data[4447]   - 80%
        - validation data[1146] - 20%  
    5. Convert doccano to spacy format
    6. Taining spacy pipeline model
    7. Evaluation Best model and get F1 Score:
        - Training Data[4483]   : 
            precision    :  0.9900669900669901
            recall       :  0.7739256049115204
            F1-Score     :  0.8687544339718253

        - Validation Data[1161] :
            precision    :  0.8253358925143954
            recall       :  0.6086341118188252
            F1-Score     :  0.7006109979633401

# Experiment - 2

    1. Tunning Hyper paramerter
    2. Adding custom word vector using Gensim
    3. Taining spacy pipeline model
    4. Evaluation Report:
      - Training Data[4483]   : 
            precision    :  0.9900669900668501
            recall       :  0.7732256049115204
            F1-Score     :  0.8667544339718253

        - Validation Data[1161] :
            precision    :  0.8153358925143954
            recall       :  0.6076341118188252
            F1-Score     :  0.6906109979633401


# Experiment - 3
    1. Change Spacy pipeline to transformer based spacy model
    2. Experiment pretrain bert model exist opensource
    3. Taining spacy transformer pipeline model with hyper parameter tunning
    4. Evaluation Report:
        - Training Data [4483]  : 
            precision    :  0.9845489661440582
            recall       :  0.782271168080881
            F1-Score     :  0.871830985915493

        - Validation Data[1161]:
            precision    :  0.8995594713656387
            recall       :  0.7225760792639774
            F1-Score     :  0.8014128728414442
        
# Experiment - 4
    1. Augment data generation and Adding Augmented data[1454]
    2. Train transformer based spacy pipeline
    4. Evaluation Report:
        - Training Data[5646] :
            precision         :  0.9908045977011494
            recall            :  0.77825929938606
            F1-Score          :  0.8717637540453074
 
        - Validation Data : 
            precision[1452]  :  0.909330985915493
            recall           :  0.7310686482661005
            F1-Score         :  0.810513927030208

# Experiment - 4
    1. Experiemnt BERT base data pipeline as well as model
    2. Experiment BERT model small to medium  
    3. Taining BERT Model
        - Training Data   : 
        - Validation Data : 

