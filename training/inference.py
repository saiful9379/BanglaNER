# pip install -U spacy
import os
import spacy
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(device)

if device=="cuda":
    spacy.require_gpu()
else:
    spacy.require_cpu()

class BanglaNER:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.model_loading()

    def model_loading(self):
        """
        """
        print(f"Model Loading {os.path.basename(self.model_path)}....:", end="", flush=True)
        
        model = spacy.load(self.model_path)
        print("Done")
        return model
    
    def prediction(self, text):

        doc = self.model(text)
        print(f"Input: {text}")
    
        data, index = {}, 0
        for entity in doc.ents:
            print(f"Entity: {entity.text}, Label: {entity.label_}")
            predicted_entities = [(ent.start_char, ent.end_char, ent.label_, ent.text) \
                                  for ent in doc.ents]
            
            if predicted_entities:
                for pe in predicted_entities:
                    per_info = {
                        "span_position" : pe[:2],
                        "cls"   : pe[2],
                        "person_name" : pe[3] 
                    }

                    data[index] = per_info
                
                    index += 1 
        print(data)
        return data

if __name__ == "__main__":

    model_path = "./models/bangla_ner_model"

    text_list = [
        "আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম",
        "নতুন বছরে জ্বলছেন আরও একজন—রজার ফেদেরার ।",
        "ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান",
        "তিনি মোহাম্মদ বাকির আল-সদর এর ছাত্র ছিলেন।",
        "লিশ ট্র্যাক তৈরির সময় বেশ কয়েকজন শিল্পীর দ্বারা অনুপ্রাণিত হওয়ার কথা স্মরণ করেন, বিশেষ করে ফ্রাঙ্ক সিনাত্রা ।",
    ]

    bner = BanglaNER(model_path)
    for i in text_list:
        bner.prediction(i)
