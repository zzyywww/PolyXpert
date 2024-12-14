#!/usr/bin/env python
#_*_coding:utf-8_*_

import os
os.environ["NCCL_P2P_DISABLE"] = "1"
os.environ["NCCL_IB_DISABLE"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import Dataset #Dataset class of hungging face
from torch.utils.data import DataLoader
from tqdm import tqdm
import sys
import time

input = sys.argv[1]#sequence file, 'Name' column for sequence id, 'VH' column for heavy chain Fv sequence,  'VL' column for light chain Fv sequence 

def create_dataset(tokenizer, df, max_length=512):
    seqs_df = df.copy()
    seqs_df["VH"] = seqs_df["VH"].str.replace('|'.join(["O", "B", "U", "Z"]), "X", regex=True)
    seqs_df["VL"] = seqs_df["VL"].str.replace('|'.join(["O", "B", "U", "Z"]), "X", regex=True)
    seqs_df['VH'] = seqs_df.apply(lambda row: " ".join(row["VH"]), axis=1)
    seqs_df['VL'] = seqs_df.apply(lambda row: " ".join(row["VL"]), axis=1)

    tokenized = tokenizer(
        list(seqs_df['VH']),
        list(seqs_df['VL']), 
        max_length=max_length,
        padding=True,
        truncation=True,
        return_tensors='pt'
    )
    dataset = Dataset.from_dict(tokenized)
    dataset = dataset.with_format("torch")
    return dataset

def model_test(model, test_loader, device):
    predictions = []
    model.to(device)
    model.eval()
    with torch.no_grad():
        for batch in tqdm(test_loader):
            input_ids = batch['input_ids'].to(device)  
            attention_mask = batch['attention_mask'].to(device)  
            # 预测
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)  

            logits = outputs.logits  

            proba = torch.softmax(logits, dim=1)
            pred_label = torch.argmax(proba, dim=1)

            for i in range(proba.size(0)): 
                predictions.append({
                    'proba_0': proba[i, 0].item(),  
                    'proba_1': proba[i, 1].item(), 
                    'pred_label':pred_label[i].item(),
                })

    predictions = pd.DataFrame(predictions)
    return predictions

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained('./PolyXpert')
trained_model = AutoModelForSequenceClassification.from_pretrained('./PolyXpert', num_labels=2)

test = pd.read_csv(input,index_col=False,sep='\t')
test_data = create_dataset(tokenizer, test)
test_loader = DataLoader(test_data, batch_size=16, shuffle=False,pin_memory=True)
predictions = model_test(trained_model,test_loader,device)
predictions.set_index(test['Name']).to_csv('./results/pred_results_'+time.strftime('%Y%m%d%H%M%S', time.localtime())+'.txt',sep='\t')
