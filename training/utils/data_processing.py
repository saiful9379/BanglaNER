"""
This is data preprocessing code for process data to BILOU format 
and discard data which are not match with labels. This code based on 
Bangla NER data processing those Banglakit, Rifat1493's, SemiEval NER data.
"""

import os
import random
import json
import six
import unicodedata
import glob
from typing import Any, List, Dict, Set
from bliou_format_correction import get_bilou_format_correction


SUPPORTED_ENTITY = {'O', 'I-PER', 'B-PER', 'U-PER', 'L-PER'}

TRAINING_PERCENTAGE = 80

NUMBER_OF_SHUFFLE = 4

class helper:
  def get_token_format(self, text, label):
    """
    
    """
    return {
        "orth": text,
        "tag":"-",
        "ner": label
        }

  def get_iob_json_template(self, id:int=None, tokens:list=None):
    '''Return standered spacy data formate for a single data point'''
    return {
            "id": id,
            "paragraphs": [{
                "sentences": [{
                    "tokens": tokens
                }]
            }]
        }
  def get_data_summary(self, data):
    class_frquency = {}
    token_index = 0
    for i in data:
      tokens = i["paragraphs"][0]["sentences"][0]["tokens"]
      # print(tokens)
      for token in tokens:
        text, label = token["orth"], token["ner"]
        if label in class_frquency:
          class_frquency[label] += 1
        else:
          class_frquency[label] = 1
        token_index+= 1

    return token_index, class_frquency

  def save_json_file(self, data, output_dir = "unknown.json"):
    with open(output_dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

  def check_biluo_format(self, i_per_index, label):
     pass


class BasicTokenizer:
  """
  Runs basic tokenization punctuation, splitting and lower casing

  Resource link for more details:
  Basic tokenization tokenize sentence using white spaces, punctuation mark
  Code shamelessly copied from BERT tokenization 
  To check Original Code: https://github.com/google-research/bert/blob/master/tokenization.py


  """
  def whitespace_tokenize(self, text:str)->List[str]:
    """
    Runs basic whitespace cleaning and splitting on a piece of text
    """
    text = text.strip()
    # print("Text: ", text)
    if not text:
        return []
    tokens = text.split()
    # print("tokens : ", tokens)
    return tokens
  
  def convert_to_unicode(self, text:str)-> str:
    """
    Converts text to Unicode assuming utf-8 .
    
    """
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text.decode("utf-8", "ignore")
        elif isinstance(text, unicode):
            return text
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")

  def _run_strip_accents(self, text:str)-> str:
    """
    Strips accents from a piece of text.
    
    """
    text = unicodedata.normalize("NFD", text)
    output = []
    for char in text:
      cat = unicodedata.category(char)
      if cat == "Mn":
        continue
      output.append(char)

    return "".join(output)
  
  def _is_punctuation(self, char:str)-> bool:
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
        (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False

  def _run_split_on_punc(self, text:str)-> List[str]:
    """Splits punctuation on a piece of text."""
    chars = list(text)
    i = 0
    start_new_word = True
    output = []
    while i < len(chars):
      char = chars[i]
      if self._is_punctuation(char):
        output.append([char])
        start_new_word = True
      else:
        if start_new_word:
          output.append([])
        start_new_word = False
        output[-1].append(char)
      i += 1

    return ["".join(x) for x in output]
  
  def tokenize(self, text):
    """
    Tokenizes a piece of text.
    
    """
    text = self.convert_to_unicode(text)
    orig_tokens = self.whitespace_tokenize(text)
    # print("original tokens: ", orig_tokens)
    split_tokens = []
    for token in orig_tokens:
        # if self.do_lower_case:
        #   token = token.lower()
        #   token = self._run_strip_accents(token)
        split_tokens.extend(self._run_split_on_punc(token))

    # print("split tokens: ", split_tokens)
    output_tokens = self.whitespace_tokenize(" ".join(split_tokens))
    return output_tokens

class BanglakitNER:
  def __init__(self, input_file):
    self.input_file = input_file

  def read_data_file(self):
    with open(self.input_file, 'r') as f:
      lines = f.readlines()
      data = [json.loads(line) for line in lines]
    return data
  
  def process_line_and_cls(self, data:List):
    '''
    Text data source which is in iob format clean it and save it as iob
    file format and keep only supported tags
    Arge:
        text_flie (str): file path of iob format text data file
        iob_file (str): clean iob file name
        save_at: where you want to save your file
    Returens:
        None
    '''
    hp = helper()
    data_list = [
      hp.get_iob_json_template(
      id=i,
      tokens=[
          hp.get_token_format(token, label.replace("PERSON", "PER") if 'PERSON' in label else 'O')
          if label not in SUPPORTED_ENTITY
          else hp.get_token_format(token, 'O')
          for token, label in zip(line[1], line[2])
        ]
    )
    for i, line in enumerate(data)
    ]
    return data_list
  
  # def jsonl_file_to_iob_format(self, data_from_json):
  def convert_to_iob_format(self):
    """
    Check data processing
    """
    # json file processing
    bst = BasicTokenizer()
    hp = helper()
    data = self.read_data_file()
    match_line = 0
    matching_data, discard_data = [], []
    for line in data:
        text, labels = line[0], line[1]
        tokens = bst.tokenize(text)
        if len(tokens) != len(labels):
            discard_data.append([text, tokens, labels])
        else:
            match_line += 1
            matching_data.append([text, tokens, labels])
    iob_data_format = self.process_line_and_cls(matching_data)
    token_index, class_frquency = hp.get_data_summary(iob_data_format)

    print("============= banglakit data processing report  =============")
    print(
       f"\t No. of Total Line  : {len(data)} \n \
        No. of Match Line with Label : {match_line}\n \
        No. of Line Not Match with Label : {len(data)-match_line}"
        )
    print("No. of Tokens : ", token_index)
    print("Label Frequency ", class_frquency)
    
    return iob_data_format
  
class Rifat1493BnNER:
  def __init__(self, input_file):
    self.input_file = input_file

  def read_data_file(self):
    with open(self.input_file, 'r', encoding='utf8') as f:
      data = f.readlines()
    return data

  def process_data_using_new_line(self, data):
    """
    read txt bangla ner data and 
    
    """
    iob_data, unique_tags = [], set()
    # data = self.read_txt_file()
    data_line = []
    for line in data:
        line = line.strip()
        line = line.strip('\n')
        # skip blank lines and invalid data sample
        if not line or len(line.split('\t')) != 2:
          data_line = []
          continue
        # take text and entity tag name
        text, tag = line.split('\t')
        if text and tag:
            unique_tags.add(tag)
            if tag not in SUPPORTED_ENTITY:
                tag = 'O'
            data_line.append(text + '\t' + tag)
        if data_line not in iob_data:
          iob_data.append(data_line)
    return iob_data
  
  
  def convert_to_iob_format(self):
    """
    Convert txt text line to IOB template format
    """
    data_list = []
    data = self.read_data_file()
    data = self.process_data_using_new_line(data)

    hp = helper()
    print(f"Total Number of line  :  {len(data)}")

    for index, line in enumerate(data):
        tokens_list = []
        text_list = [i.split("\t")[0] for i in line]
        label_list1 = [i.split("\t")[1] for i in line]

        label_list = get_bilou_format_correction(label_list1)
        for text, label in zip (text_list, label_list):
            token_template = hp.get_token_format(text, label)
            # print(token_template)
            tokens_list.append(token_template)
        iob_template = hp.get_iob_json_template(
           id = index,
           tokens = tokens_list
        )
        data_list.append(iob_template)

    token_index, class_frquency = hp.get_data_summary(data_list)


    print("\n============= rifat1493 data processing report  =============")

    print(f"No. of Total Line : {len(data)}")

    print("No. of Tokens : ", token_index)
    print("Label Frequency ", class_frquency)

    return data_list
   
class SemiEvalBnNER:
  def __init__(self, input_file):
    self.input_file = input_file
   
  def read_data_file(self, file_path):

    """
    read data file
    """
    with open(file_path, 'r') as file:
       data = json.load(file)
    return data
  
  def convert_to_iob_format(self):
    """
    process semieval file and exclude the other class without person cls
    
    """
    if isinstance(self.input_file, str):
       data = self.read_data_file(self.input_file)
    else:
      data = [
         item for file_ in self.input_file for item in self.read_data_file(file_)
         ]
      print(len(data))
    hp = helper()
    data_list = []
    for i, line in enumerate(data):
      tokens = line["paragraphs"][0]["sentences"][0]["tokens"]
      token_list = []


      # print(tokens)
      text_list = [token["orth"] for token in tokens]
      label_list = [token["ner"] for token in tokens]

      # change the label when I-PER present but abasen B-PER before the I-PER
      if "I-PER" in label_list:
        
        if label_list.index("B-PER") > label_list.index("I-PER"):
          print(label_list)
          print(label_list.index("I-PER"),  label_list.index("B-PER"))

      for text, label in zip (text_list, label_list):
        if label not in SUPPORTED_ENTITY:
          label = "O"
        token = hp.get_token_format(
           text, label
           )
        token_list.append(token)

      iob_formated_data = hp.get_iob_json_template(
         id = i,
         tokens = token_list
         )
      data_list.append(iob_formated_data)

    token_index, class_frquency = hp.get_data_summary(data_list)

    print("\n============= SemiEval data processing report  =============")

    print(f"No. of Lines    : {len(data)}")
    print(f"No. of Tokens   : {token_index}")
    print(f"Label Frequency : {class_frquency}")

    return data_list

def data_distribution(
      data:list , output_dir:str = ""
      )-> None:
  """
  This funcation perform for training and validation 
  data distribution
  """
  # initialization halper class
  hp = helper()

  token_index, class_frquency = hp.get_data_summary(data)

  print("================ Merged Data Report ===================")

  print(f"No. of Lines    : {len(data)}")
  print(f"No. of Tokens   : {token_index}")
  print(f"Label Frequency : {class_frquency}")

  for i in range(NUMBER_OF_SHUFFLE):
    print(f'Shuffling data ... {i+1} times')
    random.shuffle(data)
  print("Shuffle done ...")


  total_data = len(data)
  train_split = int((total_data * TRAINING_PERCENTAGE)/100)
  
  print(f" Total data {len(data)} Spliting number : {train_split}")
  train_data = data[:train_split]
  val_data = data[train_split:]

  print(f"No. of Training data : {len(train_data)}")
  print(f"No. of Validation data : {len(val_data)}")

  hp.save_json_file(
    train_data,
    os.path.join(output_dir, "train.json")
  )
  hp.save_json_file(
    val_data,
    os.path.join(output_dir, "val.json")
  )
   
if __name__ == '__main__':
    # output path directory
    output_dir = "./data/ner_bliou_processed_data"
    os.makedirs(output_dir, exist_ok=True)


    # make sure the dataset path
    banglakit= "./data/raw_data/banglakit/main.jsonl"
    rifat1493 = "./data/raw_data/Rifat1493_NER_txt/all_data.txt"
    semieval = "./data/raw_data/SemiEval"
    semieval_files = glob.glob(semieval+"/*.json")
    
    """
    please register your dataset which have BIO tagging or BLIOU 
    format like above above the dataset format.
    """

    register_dataset = {
       "BanglakitNER"   : banglakit,
       "Rifat1493BnNER" : rifat1493,
       "SemiEvalBnNER"  : semieval_files

    }

    method_name = "convert_to_iob_format"

    processed_data = []
    try: 
      for class_name, data_dir in register_dataset.items():
          class_obj = globals()[class_name]
          instance = class_obj(data_dir)
          # Call the method dynamically using getattr()
          if hasattr(instance, method_name):
              method = getattr(instance, method_name)
              data = method()
              processed_data+=data
          else:
              print(f"Method '{method_name}' not found.")
    except KeyError:
        print(f"Class '{class_name}' not found.")
    except TypeError as e:
        print(f"Error creating an instance: {e}")
    if processed_data:
        data_distribution(
          data = processed_data,
          output_dir = output_dir
          )
    else:
       print(f"Fatching Data processing Issue lenght of Data {processed_data}")





