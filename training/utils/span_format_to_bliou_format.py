import os
import json
import glob

def read_data_file(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().split("\n")
        data = [json.loads(line) for line in lines if line]
    return data


def save_json(data, output_dir):
    with open(output_dir, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def get_token_format(text, label):
    """
    get token format
    """
    return {
        "orth": text,
        "tag":"-",
        "ner": label
        }
def get_iob_json_template(id:int=None, tokens:list=None):
    '''Return standered spacy data formate for a single data point'''
    return {
            "id": id,
            "paragraphs": [{
                "sentences": [{
                    "tokens": tokens
                }]
            }]
        }

def convert_to_bliou(text, entities):
    bliou_format = []
    # Initialize a list to store the labels for each token
    labels = ['O'] * len(text)

    # Process each labeled entity and update the labels list
    for entity_start, entity_end, entity_type in entities:
        labels[entity_start] = 'B-' + entity_type
        print(len(labels), entity_end)
        # if len(labels) == entity_end:
        #     end = entity_end
        # else:
        #     end = entity_end+1

        for i in range(entity_start + 1, entity_end):
            # print(i)
            labels[i] = 'I-' + entity_type

    # Create the BLIOU format
    for token, label in zip(text, labels):
        bliou_format.append(f'{token}\t{label}')

    return bliou_format

def get_grouping_and_tokens_generation(my_list):
    # Split the list based on space
    result, temp_list = [], []
    for item_l in my_list:
        item = item_l.split("\t")
        if item[0] == " ":
            # Add the current sublist to the result list
            result.append(temp_list)
            # Reset the temporary list for the next sublist
            temp_list = []
        else:
            # Add the item to the current sublist
            temp_list.append(item)
    # Add the last sublist to the result (after the last space)
    result.append(temp_list)
    tokens = []
    for r in result:
        r_str = "".join([i[0] for i in r])
        cls_ = [i[1] for i in r]
        if len(cls_)==0:
            continue
        token = get_token_format(r_str, cls_[0])
        tokens.append(token)
    # print(tokens)
    return tokens

if __name__ == "__main__":
    input_dir = "./data/bangla_ner_data_with_augment"
    ouput_dir = "./data/bangla_ner_data_with_augment_bliou"

    files = glob.glob(input_dir+"/*.jsonl")

    os.makedirs(ouput_dir, exist_ok=True)

    for file in files:
        data = read_data_file(file)

        print(data)

        file_name = os.path.basename(file)

        data_list = []
        for i, line in enumerate(data):
            print(line)
            text, entities = line["text"], line["label"]
            bliou_result = convert_to_bliou(text, entities)
            tokens = get_grouping_and_tokens_generation(bliou_result)
            iob_template = get_iob_json_template(i, tokens)
            data_list.append(iob_template)

        save_json(
            data_list,
            os.path.join(ouput_dir, file_name.split["."][0]+".json")
        )
