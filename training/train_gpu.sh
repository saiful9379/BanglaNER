python -m spacy train configs/config.cfg \
    --gpu-id 0 \
    --output ./models/bangla_ner_model_v5 \
    --paths.train ./data/bangla_ner_data_with_augment/train.spacy \
    --paths.dev ./data/bangla_ner_data_with_augment/train.spacy