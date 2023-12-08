
"""
This is a preprocessing script for BLIOU Data formating checker and corrected
the worng BLIOU format.
"""

def flatten_to_nested(input_list:list)->list:
    """
    Groups consecutive tags of the same class into nested lists.
    
    Args:
        input_list (list): List of tags.

    Returns:
        list: List of nested lists where consecutive tags of the same class are grouped.
    """
    current_sequence, nested_list = [], []

    for tag in input_list:
        if tag[0].startswith("B-"):
            if current_sequence:
                nested_list.append(current_sequence)
            current_sequence = [tag]
        elif tag[0].startswith("I-") or tag[0].startswith("L-"):
            current_sequence.append(tag)
        else:
            if current_sequence:
                nested_list.append(current_sequence)
            current_sequence = []
    if current_sequence:
        nested_list.append(current_sequence)

    return nested_list

def get_class_grouping(input_sequence:list)->list:
    """
    Groups consecutive tags of the same class into lists.

    Args:
        input_sequence (list): List of tags.

    Returns:
        list: List of lists where consecutive tags of the same class are grouped.
    """
    output_sequence, final_list = [], []
    for i, tag in enumerate(input_sequence):
        if tag in {"B-PER", "I-PER", "L-PER"}:
            if len(input_sequence) - 1 == i:
                output_sequence.append([tag, i])
                final_list.append(output_sequence)
                output_sequence = []
            else:
                output_sequence.append([tag, i])
        elif tag == "O":
            if output_sequence:
                final_list.append(output_sequence)
                output_sequence = []

    return final_list



def get_bilou_format_correction(input_sequence:list)->list:
    """
    Corrects the BILOU format of the input sequence and returns the corrected sequence.

    Args:
        input_sequence (list): List of tags in BILOU format.

    Returns:
        list: Corrected list of tags in BILOU format.
    """
    final_list = get_class_grouping(input_sequence)
    for i in final_list:
        output = flatten_to_nested(i)
        if len(output) > 1:
            for j in range(len(output) - 1):
                if len(output[j]) == 1 and len(output[j + 1]) == 1:
                    cls_list, cls_index = [output[j][0][0], output[j + 1][0][0]], [output[j][0][1], output[j + 1][0][1]]
                    input_sequence[cls_index[0]] = "B-PER" if cls_list[0] in {"I-PER", "U-PER"} else input_sequence[cls_index[0]]
                    input_sequence[cls_index[1]] = "L-PER" if cls_list[1] in {"I-PER", "B-PER", "U-PER"} else input_sequence[cls_index[1]]

                else:
                    if len(output[j]) == 2 and len(output[j + 1]) == 1:
                        input_sequence[output[j][0][1]] = "B-PER" if output[j][0][0] != "B-PER" else input_sequence[output[j][0][1]]
                        input_sequence[output[j][1][1]] = "I-PER" if output[j][1][0] != "I-PER" else input_sequence[output[j][1][1]]
                        input_sequence[output[j + 1][0][1]] = "L-PER" if output[j + 1][0][0] in {"I-PER", "B-PER"} else input_sequence[output[j + 1][0][1]]

                    else:
                        cls_list1, cls_index1 = [i[0] for i in output[j]], [i[1] for i in output[j]]
                        cls_list2, cls_index2 = [i[0] for i in output[j + 1]], [i[1] for i in output[j + 1]]

                        input_sequence[cls_index1[0]] = "B-PER" if cls_list1[0] in {"I-PER", "U-PER"} else input_sequence[cls_index1[0]]
                        input_sequence[cls_index2[0]] = "B-PER" if cls_list2[0] in {"I-PER", "U-PER"} else input_sequence[cls_index2[0]]
                        input_sequence[cls_index1[-1]] = "U-PER" if cls_list1[-1] in {"I-PER", "B-PER"} else input_sequence[cls_index1[-1]]
                        input_sequence[cls_index2[-1]] = "L-PER" if cls_list2[-1] in {"I-PER", "B-PER"} else input_sequence[cls_index2[-1]]

        else:
            cls_list, cls_index  = [i[0] for i in output[0]], [i[1] for i in output[0]]

            if len(cls_list) == 1:
                input_sequence[cls_index[0]] = "U-PER" if cls_list[0] in {"I-PER", "B-PER"} else input_sequence[cls_index[0]]
            else:
                input_sequence[cls_index[0]] = "B-PER" if cls_list[0] == "I-PER" else input_sequence[cls_index[0]]
                input_sequence[cls_index[-1]] = "L-PER" if cls_list[-1] in {"I-PER", "B-PER"} else input_sequence[cls_index[-1]]

    return input_sequence

if __name__ == "__main__" : 
    
    inputs = [
        ['O', 'O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'I-PER'],
        ['O', 'O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'B-PER', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ["O", "O", "B-PER", "I-PER", "I-PER", "L-PER", "O", "O", "B-PER", "I-PER", "I-PER"],
        ["O", "O", "B-PER", "I-PER", "I-PER", "O", "O", "B-PER", "I-PER", "I-PER", "O"],
        ["O", "O", "I-PER", "I-PER", "I-PER", "O", "O", "O"],
        ["O", "O", "B-PER", "I-PER", "I-PER", "O", "O", "O"],
        ["O", "O", "B-PER", "B-PER", "O", "O", "O"],
        ["O", "O", "I-PER", "I-PER", "O", "O", "O"],
        ["O", "O", "B-PER", "O", "O", "O"],
        ["O", "O", "I-PER", "O", "O", "O"],
        ["O", "O", "I-PER", "I-PER", "O", "O", "O"],
        ["O", "O", "I-PER", "I-PER", "O", "O", "O","I-PER", "I-PER"],
        ["O", "I-PER", "O", "I-PER", "O", "O", "O"],
        ["B-PER", "I-PER", "I-PER", "I-PER", "O", "O", "O"],
        ["B-PER", "I-PER", "B-PER", "I-PER", "O", "O", "O"]
    ]

    output_results = [get_bilou_format_correction(seq) for seq in inputs]

