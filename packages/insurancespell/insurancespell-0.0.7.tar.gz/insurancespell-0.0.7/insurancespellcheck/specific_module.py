from storage import mydict, custom_subwords
from pythainlp import subword_tokenize
import re

# replace show correct word
def replace_correct_words(text: str, dictionary: dict = mydict):
    # Define a regex pattern to match the incorrect word within <คำผิด> tags
    pattern = re.compile(r'<คำผิด>(.*?)</คำผิด>')

    # Find all matches in the input string
    matches = pattern.findall(text)

    # Iterate over matches
    for match in matches:
        # Iterate over dictionary items
        for key, values in dictionary.items():
            # Check if the match is in the list of incorrect words
            if match in values:
                # Replace the incorrect word with the correct word
                replacement = key
                text = text.replace(f'<คำผิด>{match}</คำผิด>', replacement)
    return text

# get specific correct word
# return list
def get_correct_words(text: str, dictionary: dict = mydict):
    correct_words = []
    # Define a regex pattern to match the incorrect word within <คำผิด> tags
    pattern = re.compile(r'<คำผิด>(.*?)</คำผิด>')
    # Find all matches in the input string
    wrong_word = pattern.findall(text)
    for key, values in dictionary.items():
        for value in values:
            if value in wrong_word:
                correct_words.append(key)
    # return correct not duplicates
    return "\n".join(x for x in list(set(correct_words)))



## Tokenize subword
def tokenize_subword(text):
	return subword_tokenize(text, engine='dict', keep_whitespace=False)
##push mykey to subword
for key in custom_subwords.keys():
	custom_subwords[key] = tokenize_subword(key)
