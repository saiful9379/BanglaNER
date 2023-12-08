python -m spacy train configs/config_cpu.cfg \
    --output ./models/bangla_ner_model_v1 \
    --paths.train ./data/ner_spanbased_process_data/train.spacy \
    --paths.dev ./data/ner_spanbased_process_data/val.spacy