import json
import glob
import os

def read_data_file(input_file):

    """
    read jsonl data
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    data = [json.loads(line) for line in lines]

    return data


def save_jsonl(data, output_dir):
    """
    save jsonl file
    """
    with open(output_dir, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

def data_processing(jsonl_files, output_file):

    """
    
    Augmented data filtering and exclude other class
    
    """
    data_list = []
    index = 0
    for file_ in jsonl_files:
        if os.path.basename(file_)!= "Bangla_NER5.jsonl":
            continue
        data = read_data_file(file_)
        for i in data:
            label = i["label"]
            per_label = []
            for l in label:
                if "PERSON" == l[2]:
                    per_label.append(l)

            if per_label:
                line_dict = {"text": i["text"], "label": per_label}
                data_list.append(line_dict)
                index += 1

    print(data_list)
    print(len(data_list))

    train_lenght = int((len(data_list) * 80)/100)

    train_data = data_list[:train_lenght]
    val_data = data_list[train_lenght:]

    save_jsonl(train_data, os.path.join(output_file, "train.jsonl"))
    save_jsonl(val_data, os.path.join(output_file, "val.jsonl"))






if __name__ == "__main__":

    data_path = "/media/sayan/hdd/NLP/BanglaNER/augment_data"

    output_file = "./data/augment_data"

    jsonl_files = glob.glob(data_path+"/*.jsonl")

    data_processing(jsonl_files, output_file)