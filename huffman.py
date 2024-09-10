from __future__ import annotations
from typing import List, Optional


class HuffmanNode:
    def __init__(self, char_ascii: int, freq: int, left: Optional[HuffmanNode] = None, right: Optional[HuffmanNode] = None):
        self.char_ascii = char_ascii    # stored as an integer - the ASCII character code value
        self.freq = freq                # the frequency associated with the node
        self.left = left                # Huffman tree (node) to the left!
        self.right = right              # Huffman tree (node) to the right

    def __lt__(self, other: HuffmanNode) -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    if a.freq < b.freq:
        return True
    elif a.freq > b.freq:
        return False
    if a.char_ascii <= b.char_ascii:
        return True
    return False



def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    if a < b:
        if a.char_ascii <= b.char_ascii:
            return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
        else:
            return HuffmanNode(b.char_ascii, a.freq + b.freq, a, b)
    if a.char_ascii <= b.char_ascii:
        return HuffmanNode(a.char_ascii, a.freq + b.freq, b, a)
    else:
        return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""


def cnt_freq(filename: str) -> List:
    temp_file = None
    try:
        temp_file = open(filename, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File can not be found")
    file_text = temp_file.read()
    temp_file.close()
    occur: List = [0] * 256
    for i in range(len(file_text)):
        occur[ord(file_text[i])] += 1
    return occur
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""


def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    node_list = create_node_list(char_freq)
    i = 0
    while len(node_list) > 1:
        c1 = find_min(node_list, -1)
        c2 = find_min(node_list, c1)
        new_node = combine(node_list[c1], node_list[c2])
        if c2 > c1:
            node_list.pop(c2)
            node_list.pop(c1)
            node_list.insert(c1, new_node)
        else:
            node_list.pop(c1)
            node_list.pop(c2)
            node_list.insert(c2, new_node)
        i += 1
    if len(node_list) > 0:
        return node_list[0]
    return None
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""


def find_min(node_list: List, avoid: int) -> int:
    min_index = -1
    for i in range(len(node_list) - 1, -1, -1):
        if i != avoid:
            if min_index == -1 or node_list[i] < min_node:
                min_index = i
                min_node = node_list[i]
    return min_index
    """Finds minimum value in node_list and returns it back to
    the create tree method"""


def create_node_list(char_freq: List) -> List:
    node_list = list()
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            node_list.append(HuffmanNode(i, char_freq[i], None, None))
    return node_list
    """Removes all the 0s from the node list"""


def create_code(node: Optional[HuffmanNode]) -> List:
    ret_list: List = [0] * 256
    create_code_helper(node, "", ret_list)
    return ret_list
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""


def create_code_helper(node: Optional[HuffmanNode], code: str, ret_list: List) -> None:
    if node is None:
        return
    if node.left is None and node.right is None:
        ret_list[node.char_ascii] = code

    create_code_helper(node.left, code + "0", ret_list)
    create_code_helper(node.right, code + "1", ret_list)
    """Helper method for create code that recursively adds codes
    to an array indexed at the correct ASCII value"""


def create_header(freqs: List) -> str:
    if freqs is None:
        return
    code = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            code += str(i) + " " + str(freqs[i]) + " "
    return code[0: len(code) - 1]
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """


def huffman_encode(in_file: str, out_file: str) -> None:
    try:
        temp_read_file = open(in_file, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File can not be found")
    temp_write_file = open(out_file, "w")
    freqs = cnt_freq(in_file)
    temp_write_file.write(create_header(freqs) + "\n")
    temp_write_file.close()
    code_list = create_code(create_huff_tree(freqs))
    process = temp_read_file.read()
    temp_read_file.close()
    temp_write_file = open(out_file, "a")
    for i in range(len(process)):
        temp_write_file.write(code_list[ord(process[i])])
    temp_write_file.close()
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""


def parse_header(header_string: str) -> List:
    freq_list: List = [0] * 256
    done = False
    while not done:
        index1 = header_string.find(" ")
        pos = int(header_string[0: index1])
        header_string = header_string[index1 + 1: len(header_string)]
        index2 = header_string.find(" ")
        if index2 == -1:
            index2 = len(header_string)
        freq = int(header_string[0: index2])
        if index2 + 1 < len(header_string):
            header_string = header_string[index2 + 1: len(header_string)]
        else:
            done = True
        freq_list[pos] = freq
    return freq_list

def huffman_decode(encoded_file, decode_file) -> None:
    try:
        temp_read_file = open(encoded_file, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File can not be found")
    first_line = temp_read_file.readline().strip('\n')
    if first_line == '':
        temp_write_file = open(decode_file, "w")
        temp_write_file.close()
        temp_read_file.close()
    else:
        freq_list = parse_header(first_line)
        hn = create_huff_tree(freq_list)
        if hn.left is None and hn.right is None:
            for i in range(len(freq_list)):
                if freq_list[i] != 0:
                    temp_write_file = open(decode_file, "w")
                    for j in range(freq_list[i]):
                        temp_write_file.write(chr(i))
                    temp_write_file.close()
                    i = len(freq_list)
            temp_read_file.close()
        else:
            temp_hn = hn
            second_line = temp_read_file.readline().strip('\n')
            temp_read_file.close()
            temp_write_file = open(decode_file, "w")
            for i in range(len(second_line)):
                if second_line[i] == "1":
                    temp_hn = temp_hn.right
                elif second_line[i] == "0":
                    temp_hn = temp_hn.left
                if temp_hn.left is None and temp_hn.right is None:
                    temp_write_file.write(chr(temp_hn.char_ascii))
                    temp_hn = hn
            temp_write_file.close()





