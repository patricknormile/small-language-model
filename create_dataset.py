import re
from typing import List

def tokens_row(words) :
    """
    take a row of tokenized text (from a message)
    and make a dataset of tokens + next
    """
    n = len(words)
    for i in range(1, n) :
        yield words[:i], words[i]

def make_rows_from_chat(chat : str) -> List[str]:
    """
    given a whatsapp chat, make the rowwise dataset of messages (as a list)
    """
    split_char = r"\n\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2} - "
    rows = re.split(split_char, chat)
    omitted = r"<Media omitted>"
    removed = r"removed \+?[\(\)0-9 ]{9,}"
    joined = r"joined using this group's invite link"
    filter_regex = f"{omitted}|{removed}|{joined}"
    name_number_note = r"(^[a-zA-Z0-9\+\(\) \-]+\: )|(<?This message was \w+>?$)"
    rows_filtered = [re.sub(name_number_note,"",x) for x in rows if re.search(filter_regex, x) is None]
    return rows_filtered

if __name__=="__main__":
    file_name = "artifacts/input_text.txt"
    with open(file_name, 'r') as file :
        chat = file.read()
