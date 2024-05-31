import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer

def tokens_row(words) :
    """
    take a row of tokenized text (from a message)
    and make a dataset of tokens + next
    """
    n = len(words)
    for i in range(1, n) :
        yield words[:i], words[i]

tokenizer = RegexpTokenizer('\w+')
file_name = "artifacts/input_text.txt"
with open(file_name, 'r') as file :
    chat = file.read()

split_char = r"\n\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2} - "
rows = re.split(split_char, chat)

omitted = r"<Media omitted>"
removed = r"removed \+?[\(\)0-9 ]{9,}"
joined = r"joined using this group's invite link"
filter_regex = f"{omitted}|{removed}|{joined}"
name_number_note = r"(^[a-zA-Z0-9\+\(\) \-]+\: )|(<?This message was \w+>?$)"
rows_filtered = [re.sub(name_number_note,"",x) for x in rows if re.search(filter_regex, x) is None]
rows_filtered = [tokenizer.tokenize(x) for x in rows_filtered if x != 'null']
word_chains = [[*tokens_row(x)] for x in rows_filtered]
from transformers import RobertaTokenizerFast
tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base',max_length=128)

# df=pd.DataFrame(word_chains, columns=['text','next'])
# df.to_csv("artifacts/t_text_df.csv")
print(tokenizer(rows_filtered[-1]))