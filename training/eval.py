import os
import spacy
import csv 
import json
from tqdm import tqdm
from collections import defaultdict
from seqeval.metrics import classification_report, accuracy_score
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)

ENTITY_LIST = ['PER']

if device=="cuda":
    spacy.require_gpu()
else:
    spacy.require_cpu()


class BanglaNerSpacy:
    def __ini__(self):
        pass
    # Load the SpaCy model
    def model_loading(self, model_path):
        """
        load bangla ner model
        
        """
        model = spacy.load(model_path)
        return model
    
    def read_data(self, data_path:str)->str:
        """
        data reading
        """
        with open(data_path) as f:
            data = f.read().split("\n")
        data = [json.loads(i) for i in data if i]
        return data
    
    def model_pediction(self, model, sentence):
        doc = model(sentence)
        return doc

class SeqEvalEvaluation:

    def __init__(self,  model, model_type ):
        self.model = model
        self.model_type = model_type

    def model_inference(self, data):
        # model_type_list = ["spacy", "bert"]
        if self.model_type == "spacy":
            bns = BanglaNerSpacy()
            for d in data:
                sentence = d
                doc = bns.model_pediction(self,model, sentence)

        elif self.model_type=="bert":
            print("not process yet")




    def performance_calculation(self, gt_labels, pt_labels):


        # Example data (replace this with your actual data)
        true_labels = [['B-PER', 'I-PER', 'O', 'B-LOC', 'O'],
                    ['O', 'B-ORG', 'I-ORG', 'O', 'B-PER', 'I-PER', 'O']]

        predicted_labels = [['B-PER', 'I-PER', 'O', 'B-LOC', 'O'],
                            ['O', 'B-ORG', 'I-ORG', 'O', 'B-PER', 'I-PER', 'O']]

        # Evaluate accuracy
        accuracy = accuracy_score(true_labels, predicted_labels)
        print(f'Accuracy: {accuracy:.2%}')

        # Evaluate precision, recall, and F1-score
        report = classification_report(true_labels, predicted_labels)
        print("Classification Report:\n", report)

    

class SPanBasedEval:
    def __init__(self, output_dir, debug= False):
        self.log_dir = output_dir
        self.debug = debug

    def write_log_file(self, data, output_dir):
        """
        Write data to a CSV log file.

        Parameters:
            - data (list): A list of lists, where each inner list represents a row of data.
                    The first row is considered as the header.
            - output_dir (str): The directory path along with the filename where the CSV file will be saved.

        Returns:
            None

        Example:
        ```
            data = [["Text1", "GroundTruth1", "Prediction1"],
                    ["Text2", "GroundTruth2", "Prediction2"]]
            output_dir = "/path/to/log_file.csv"
            instance.write_log_file(data, output_dir)
        ```

        The function opens a CSV file at the specified `output_dir` in write mode,
        writes the header and data to the file, and then closes the file.

        Note: If the file already exists, it will be overwritten.

        """
        with open(output_dir, mode="w", newline="", encoding="utf-8") as f:
            header = ["Text", "GT", "PT"]
            writer = csv.writer(f)
            writer.writerow(header) 
            writer.writerows(data)

    def performance_calculation(self, model, data):

        """
        Evaluate the performance of a Bangla Named Entity Recognition (NER) model using provided data.

        Parameters:
            - model: SpaCy NER model for Bangla language.
            - data (list): List of tuples, where each tuple contains a sentence and its corresponding annotation.
            - report_logs (str): File path to save the evaluation report in CSV format.
            - performance_logs (str): File path to save the entity-wise performance metrics in CSV format.

        Returns:
            None
        """
        entity_performance = defaultdict(dict)
        inference_logs = []
        for d in tqdm(range(len(data))):
            i = data[d]
            sentence, annotation = i["text"], i["label"]

            bner = BanglaNerSpacy()
            doc = bner.model_pediction(model, sentence)

            gt_entities = annotation
            gt_dict  = {i : [] for i in ENTITY_LIST}
            pt_dict = {i : [] for i in ENTITY_LIST}

            predicted_entities = [(ent.start_char, ent.end_char, ent.label_, ent.text) \
                                  for ent in doc.ents]
            
            gt = [(i[0], i[1], i[2], sentence[i[0]:i[1]]) for i in gt_entities]
            for pi in predicted_entities:
                if pi[2] in pt_dict:
                    pt_dict[pi[2]].append(pi[3])

            for gi in gt:
                if gi[2] in gt_dict:
                    gt_dict[gi[2]].append(gi[3])

            gt_en = [value if value else "" for key, value in gt_dict.items()]
            pt_en = [value if value else "" for key, value in pt_dict.items()]
            for label in ENTITY_LIST:  # Specify the entity labels of interest
                tp = sum(1 for entity in predicted_entities if entity[2] == label and entity in gt)
                fp = sum(1 for entity in predicted_entities if entity[2] == label and entity not in gt)
                fn = sum(1 for entity in gt if entity[2] == label and entity not in predicted_entities)

                entity_performance[label]["tp"] = entity_performance[label].get("tp", 0) + tp
                entity_performance[label]["fp"] = entity_performance[label].get("fp", 0) + fp
                entity_performance[label]["fn"] = entity_performance[label].get("fn", 0) + fn
                inference_logs.append([sentence, gt_en, pt_en])

        report = []
        for label in ENTITY_LIST:  # Specify the entity labels of interest
            tp = entity_performance[label].get("tp", 0)
            fp = entity_performance[label].get("fp", 0)
            fn = entity_performance[label].get("fn", 0)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            report.append([label, precision,recall, f1_score])
            print("-"*20)
            print("Label class  : ", label)
            print("precision    : ", precision)
            print("recall       : ", recall)
            print("F1-Score     : ", f1_score)

        if self.debug:
            self.write_log_file(inference_logs, self.log_dir)

if __name__ == "__main__":

    evaluation_model = "spacy"

    """
    For custom span based evalution gt data format(JSONL)look like ,

    Example, 

    {"text": "ধানমন্ডি এলাকাবাসীদের কথা চিন্তা করে এই উদ্যোগ নেন সায়মা ।", "label": [[51, 55, "PER"]]}

    OR 
    seqeval used BILOU(JSONL) format,
    Example, 
    ["আফজালুর রহমান নামের এক পরীক্ষার্থী বলেন, সবার হাতে হাতে প্রশ্ন দেখে তিনি ভেবেছিলেন এটি ভুয়া প্রশ্ন।", \
        ["B-PERSON", "L-PERSON", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]]

    """
    evaluation_modules = ["seqeval", "custom_span"]

    # model_path = "./models/bangla_ner_model_v4/model-best"

    model_path = "./models/bangla_ner_model"
    data_path = "./data/ner_spanbased_process_data/train.jsonl"

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok= True)
    selected_module = evaluation_modules[1]

    # spacy model loading
    print(f"Model Loading {os.path.basename(model_path)}....", end="", flush=True)
    bner = BanglaNerSpacy()
    model = bner.model_loading(model_path)

    print("Done")

    data = bner.read_data(data_path)
    # span based model performance
    if selected_module== "seqeval":
        see = SeqEvalEvaluation(model, evaluation_model)
    else:
        sbe = SPanBasedEval(output_dir=log_dir)
        sbe.performance_calculation(model, data)

    

