import re
import random
import numpy as np
import editdistance
import difflib
from IPython.display import display, HTML

def show_string_diffs(s1, s2):
    # Get list of differences
    differ = difflib.Differ()
    diff_list = list(differ.compare(s1, s2))

    # Define HTML wrappers
    red_wrapper = "<span style='background-color: #FFA07A'>{}</span>"
    green_wrapper = "<span style='background-color: #98FB98'>{}</span>"

    # Initialize lists to hold processed words
    s1_highlighted = []
    s2_highlighted = []

    # Process differences
    for diff in diff_list:
        if diff.startswith('- '):
            s1_highlighted.append(red_wrapper.format(diff[2:]))
        elif diff.startswith('+ '):
            s2_highlighted.append(green_wrapper.format(diff[2:]))
        elif diff.startswith('  '):
            s1_highlighted.append(diff[2:])
            s2_highlighted.append(diff[2:])

    # Display the highlighted sentences
    display(HTML(''.join(s1_highlighted)))
    display(HTML(''.join(s2_highlighted)))

def clean_up_english_spaces(string):
    """for a normal english sentence, check missing 
       trailing spaces after punchations, add if missing,
       check extra spaces before punchations, remove if extra
       no matter how many spaces between words, replace with one space
        remove leading and trailing spaces
    :param string: input sentence
    :type string: str
    """
    if not string:
        return string
    string = re.sub('\s{2,}', ' ', string)
    if string[-1] == " ":
        string = string[:-1]
    if not string:
        return string
    if string[0] == " ":
        string = string[1:]
    string = re.sub('([.,!?()])', r'\1 ', string)
    string = re.sub('\s([.,!?()])', r'\1', string)
    string = re.sub('\s{2,}', ' ', string)


    return string


def is_chinese_char(char):
    """
    check if a unicode char is a chinese char
    """
    return char >= u'\u4e00' and char <= u'\u9fff'

def string_has_chinese(string):
    """
    check if string has chinese char using regex
    """
    return bool(re.search('[\u4e00-\u9fff]', string))

def random_permute_string(string,n_times=3):
    """for a string, divide it into 3 parts, and switch the order of the 2nd and 3rd parts, repeat n times

    Args:
        string (_type_): _description_
    """
    if not string:
        return string
    for i in range(n_times):
        # get random position
        position = random.randint(0,len(string)-1)
        # get 3 parts
        part1 = string[:position]
        part2 = string[position:]
        # get 2 parts
        position2 = random.randint(0,len(part2)-1)
        part2_1 = part2[:position2]
        part2_2 = part2[position2:]
        # switch
        string = part1 + part2_2 + part2_1
    return string


def add_noise_to_string(string,n_edits,action_dist = {},skip_chars = [" ",",","."]):
    """random edit string n times, edits include replacements, deletions and insertions

    Args:
        string (_type_): input string
        n_edits (int): number of edits
        dist_config (dict, optional): distribution config for edits. Defaults to None.
    """
    default_action_dist = {"replace":0.6,
                           "delete":0.2,
                           "insert":0.2}
    lexicon = "abcdefghijklmnopqrstuvwxyz"
    # overwrite
    for k,v in action_dist.items():
        default_action_dist[k] = v
    action_dist = default_action_dist
    # get edit positions
    for i in range(n_edits):
        position = random.randint(0,len(string)-1)
        if string[position] in skip_chars:
            continue
        # get edit type
        edit_type = random.choices(list(action_dist.keys()),weights = list(action_dist.values()))[0]
        if edit_type == "replace":
            # get replacement, keep Capitalization
            if string[position].isupper():
                replacement = random.choice(lexicon).upper()
            else:
                replacement = random.choice(lexicon)
            while replacement == string[position]:
                replacement = random.choice(string)
            # replace
            string = string[:position] + replacement + string[position+1:]
        elif edit_type == "delete":
            # delete
            string = string[:position] + string[position+1:]
        elif edit_type == "insert":
            # get insertion, dont insert if previous char is space
            if string[position-1] == " ":
                continue
            insertion = random.choice(lexicon)
            # insert
            string = string[:position] + insertion + string[position:]
    return string

def text_scramble_distribute_1(string):
    """given a string, calculate the number of edits to be made to the string for text scramble

    Args:
        string (_type_): orig string, used to get len

    Returns:
        int: num of edits to make is kind of scrambled
    Examples:
        for i in range(100):
            string = "hello world, 209 of these updates are standard security updates."
            # weighted sample
            n_char = text_scramble_distribute_1(string)
            # print(n_char)
            string = add_noise_to_string(string,int(n_char))
            print(string)



    """
    replace_dist = [[0.03,10000],[0.1,1000],[0.2,100],[0.5,10],[0.8,10]]
    pick_probablity = random.choices([x[0] for x in replace_dist], weights = [x[1] for x in replace_dist])[0]
    n_char = np.random.binomial(n=len(string), p=pick_probablity, size=1)[0]
    if random.random()<0.1:
        n_char = max(n_char,1)
    return n_char





def find_least_edit_substring(string,query):
    """given a string and a substring, find begin and end index
       in string that has least edits to make substring

    Args:
        string (string): source string, the longer one
        query (string): query string, the shorter one

    Returns:
        tuple: (begin_idx, end_idx, num_edits)
               string[begin_idx:end_idx] is the substring with least edits
    """
    # init
    begin_idx = 0
    end_idx = len(query)
    min_edits = len(query)
    # loop
    for i in range(len(string)-len(query)+1):
        substring = string[i:i+len(query)]
        edits = editdistance.eval(substring,query)
        if edits < min_edits:
            begin_idx = i
            end_idx = i+len(query)
            min_edits = edits
    return (begin_idx,end_idx,min_edits)


