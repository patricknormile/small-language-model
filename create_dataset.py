import re
import pickle
import pandas as pd

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
rows_filtered = [x for x in rows_filtered if x != 'null']

with open("artifacts/t_text_list.pickle","wb") as file :
    pickle.dump(rows_filtered, file, protocol=pickle.HIGHEST_PROTOCOL)

df=pd.DataFrame(pd.Series(rows_filtered), columns=['text'])
df.to_parquet("artifacts/t_text_df.parquet")
