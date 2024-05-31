import sys
import os
import pickle
import torch
import math
from tempfile import TemporaryDirectory
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from torch.utils.data import dataset
from torchtext.datasets import WikiText2
from torchtext.data.utils import get_tokenizer
from datasets import Dataset
import mlflow
from transformers import Trainer, TrainingArguments


directory = os.path.dirname(os.path.abspath(__file__))
if directory not in sys.path:
    sys.path.append(directory)

from transformer_code import PositionalEncoding
from transformers import RobertaTokenizerFast
tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base',max_length=128)
vocab=RobertaTokenizerFast.vocab

def data_process(raw_text_iter: dataset.IterableDataset) -> Tensor:
    """Converts raw text into a flat Tensor."""
    data = [torch.tensor(vocab(tokenizer(item)), dtype=torch.long) for item in raw_text_iter]
    return torch.cat(tuple(filter(lambda t: t.numel() > 0, data)))

def tokenization(batched_text):
    batch = tokenizer(batched_text['text'], padding = True, truncation=True)
    return batch


def create_dataset(df):
    ds = Dataset.from_pandas(df)
    ds = ds.map(tokenization, batched = True, batch_size = ds.shape[0])
    ds.set_format('torch', columns=['input_ids', 'attention_mask'])
    ds = ds.train_test_split(test_size=0.3)
    return ds

# ``train_iter`` was "consumed" by the process of building the vocab,
# so we have to create it again
# with open("artifacts/t_text_list.pickle","rb") as file:
#     data = pickle.load(file)
data = pd.read_parquet("artifacts/t_text_df.parquet")
dataset = create_dataset(data)


device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

print(len(data))