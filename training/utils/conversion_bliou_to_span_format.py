
import os
import json
import glob

class SpanBasedProcessing:
    def __init__(self):
        self.search_tag = ['PER']

    def read_data_file(self, file_path):
        """
        Read data from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict: Loaded data from the JSON file.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def save_jsonl(self, data, filename):
        """
        Save data to a JSONL file.

        Args:
            data (list): List of data items.
            filename (str): Path to the output JSONL file.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for item in data:
                json.dump(item, file, ensure_ascii=False)
                file.write('\n')

    def extract_entity_positions(self, tags, search_tag):
        """
        Extract entity positions from a list of tags.

        Args:
            tags (list): List of tags.
            search_tag (str): Tag to search for.

        Returns:
            list: List of dictionaries containing start and end positions of entities.
        """
        org_positions = []
        start_pos, end_pos = None, None
        for i, tag in enumerate(tags):
            if tag == f'B-{search_tag}':
                start_pos = i
            elif tag == f'L-{search_tag}':
                end_pos = i
                if start_pos is not None:
                    org_positions.append({f"{search_tag}": [start_pos, end_pos]})
                    start_pos, end_pos = None, None
            elif tag == f'U-{search_tag}':
                org_positions.append({f"{search_tag}": [i]})
        return org_positions

    def find_string_positions(self, input_text, search_string):
        """
        Find start and end positions of a search string in the input text.

        Args:
            input_text (str): Input text.
            search_string (str): String to search for.

        Returns:
            tuple: Start and end positions of the search string.
        """
        start_position = input_text.find(search_string)
        end_position = start_position + len(search_string) - 1
        return start_position, end_position

    def get_nearest_postion_index(self, a_position, b_position):
        """
        Get the indices of nearest positions between two lists.

        Args:
            a_position (list): List of positions.
            b_position (list): List of positions.

        Returns:
            tuple: Indices of the nearest positions.
        """
        a_index = 0
        data_dict = {}
        for ap in a_position:
            b_index = 0
            for bp in b_position:
                key = f"{a_index}_{b_index}"
                data_dict[key] = abs(bp[0] - ap[1])
                b_index += 1
            a_index += 1
        min_key = min(data_dict, key=data_dict.get)
        r_index = list(map(int, min_key.split("_")))
        return a_position[r_index[0]], b_position[r_index[1]]

    def get_near_position(self, input_text, search_string_list):
        """
        Get nearest positions of multiple search strings in the input text.

        Args:
            input_text (str): Input text.
            search_string_list (list): List of search strings.

        Returns:
            list: List of nearest positions.
        """
        positions = {}
        word_position_list = []
        for word in search_string_list:
            start = -1
            while True:
                start = input_text.find(word, start + 1)
                if start == -1:
                    break
                end = start + len(word) - 1
                if word in positions:
                    positions[word].append((start, end))
                else:
                    positions[word] = [(start, end)]
        position_list = [[word, matches] for word, matches in positions.items()]
        for index in range(len(position_list) - 1):
            a, b = self.get_nearest_postion_index(position_list[index][1], position_list[index + 1][1])
            word_position_list.extend([a, b])
        return sorted(list(set(word_position_list)))

    def span_position_finding(self, text, tokens, entity_positions):
        """
        Find span positions based on entity positions.

        Args:
            text (str): Input text.
            tokens (list): List of tokens.
            entity_positions (list): List of dictionaries containing entity positions.

        Returns:
            list: List of span positions.
        """
        list_of_category = []
        for e_p in entity_positions:
            category = list(e_p.keys())[0]
            p_range = e_p[category]
            if len(p_range) == 1:
                value = p_range[0]
                before_token = tokens[:value]
                start_position, end_position = self.find_string_positions(text, tokens[value])
                list_of_category.append([start_position, end_position, category])
            else:
                l_token = tokens[p_range[0]:p_range[1] + 1]
                word_span = self.get_near_position(text, l_token)
                start_position, end_position = word_span[0][0], word_span[-1][1] + 1
                list_of_category.append([start_position, end_position, category])
        return list_of_category

    def bliou_to_spanbased_conversion(self, data_path: str = None):
        """
        Convert BLIOU formatted data to span-based format.

        Args:
            data_path (str): Path to the BLIOU formatted data file.

        Returns:
            list: List of span-based formatted data.
        """
        data = self.read_data_file(data_path)
        data_list = []
        index = 0
        for i, line in enumerate(data):
            
            per_entity_status = False
            
            tokens = line["paragraphs"][0]["sentences"][0]["tokens"]
            text_list = [token["orth"] for token in tokens]
            label_list = [token["ner"] for token in tokens]
            text = " ".join(text_list)
            for tag in self.search_tag:
                entity_positions = self.extract_entity_positions(label_list, tag)
                if entity_positions:
                    list_of_category = self.span_position_finding(text, text_list, entity_positions)
                    data_list.append({"text": text, "label": list_of_category})
                    index += 1
                    per_entity_status = True

            if per_entity_status == False:
                pass
                # print(text_list)
                # print(label_list)


        print(f"Total number of line : {len(data)}")
        print(f"Person Entity Found  : {index}")
        return data_list


if __name__ == '__main__':

    #make sure input path directory
    data_path = "./data/bangla_ner_data_with_augment"
    #make sure output path directory  
    output_dir = "./data/bangla_ner_data_with_augment"

    json_files = glob.glob(data_path+"/*.json")
    os.makedirs(output_dir, exist_ok=True)

    sbp = SpanBasedProcessing()
    for file_path in json_files:
        file_name = os.path.basename(file_path)
        
        output_file = os.path.join(output_dir, file_name.split(".")[0]+".jsonl")
        print(f"procesed file : {output_file}")
        data_list = sbp.bliou_to_spanbased_conversion(data_path=file_path)
        sbp.save_jsonl(data_list, output_file)


