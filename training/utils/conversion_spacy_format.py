import os
import json
import spacy
from tqdm import tqdm
from spacy.tokens import DocBin

VISUALIZATION_STATUS = False


def save_jsonl(data, output_dir):
    """
    Save a list of data into a JSON Lines file.

    Parameters:
        - data (list): List of data to be saved.
        - filename (str): The name of the file to save.

    Returns:
        None
    """
    with open(output_dir, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

def read_jsonl_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read().split("\n")
    data = [json.loads(line) for line in data if line]
    return data



def convert_spacy_format(data, output_path="data/unkonwn.spacy"):
    """
    Convert data to Spacy format and save it as a DocBin.

    Parameters:
        - data (list): List of tuples containing text and annotations.
        - output_path (str): The path to save the Spacy DocBin file.

    Returns:
        None
    """
    nlp = spacy.blank("bn") # load a new spacy model
    db = DocBin() # create a DocBin object
    number_of_skip_entity, processed_line = 0, 0
    for text, annot in tqdm(data): # data in previous format
        try:
            doc = nlp.make_doc(text) # create doc object from text
            ents = []
            for start, end, label in annot["entities"]: # add character indexes
                
                span = doc.char_span(start, end, label=label, alignment_mode="strict")
                # print(start, end, label, span)
                if span is None:
                    s = doc.text
                    sub_E = s[end:]
                    sub_S = s[:start]
                    end = end+ (0 if len(sub_E.split(" ", 1)[0]) <= 0 else len(sub_E.split(" ", 1)[0]))
                    start = start - (0 if len(sub_S.rsplit(" ", 1)[-1]) <= 0 else len(sub_S.rsplit(" ", 1)[-1]))
                    
                    span = doc.char_span(start, end, label=label, alignment_mode="strict")
                    if span is None:
                        number_of_skip_entity += 1
                        # print("++++++++++++++++++++++++++++Skipping entity Start++++++++++++++++++++++++++++")
                        # print(start, end, label, span)
                        # print(doc.text[start:end],doc.text[start],doc.text[end],'kh',sep='|')
                        # print("++++++++++++++++++++++++++++Skipping entity End++++++++++++++++++++++++++++++")
                        break
                else:
                    processed_line += 1
                    ents.append(span)
            doc.ents = ents # label the text with the ents
            if VISUALIZATION_STATUS:
                spacy.displacy.render(doc, style="ent", jupyter=True)
            db.add(doc)
        except:
            number_of_skip_entity += 1 
    db.to_disk(output_path) # save the docbin object

    print(f" Spacy Processed file   : {output_path}")
    print(f" No. of Processed line : {processed_line}")
    print(f" No. of Skip Entity  : {number_of_skip_entity}")



def data_convert_spacy_format(file_path):
    """
    Convert data from a JSON Lines file to Spacy format.

    Parameters:
        - jsonl_file_path (str): The path to the JSON Lines file.

    Returns:
        - training_data (list): List of tuples containing text and annotations.
    """
    # need to check empty line
    training_data, lines=[], []
    # with open(jsonl_file_path, 'r') as f:
    #     data = f.read().split("\n")
    # # print(data)
    # for line in data:
    #     j_line = json.loads(line)
    data = read_jsonl_file(file_path)
    for line in data:
        text, entities= line['text'], line['label']
        if len(entities)>0:
            training_data.append((text, {"entities" : entities}))
    return training_data



if __name__ == "__main__":
    import glob
    input_dir = "./data/bangla_ner_data_with_augment"
    output_dir = "./data/bangla_ner_data_with_augment"

    jsonl_files = glob.glob(input_dir+"/*.jsonl")
    for jsonl_file in jsonl_files:
        file_name = os.path.basename(jsonl_file).split(".")[0]+".spacy"
        data = data_convert_spacy_format(jsonl_file)
        convert_spacy_format(data, output_path=os.path.join(output_dir, file_name))
    
